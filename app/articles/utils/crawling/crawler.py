import asyncio
import re

import aiohttp
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from articles.utils.crawling.driver import set_headless_driver
from ...models import Keyword, Article, Writer


class Crawler:
    def __init__(self, keyword=None, writer=None):
        self.keyword = keyword
        self.user_id = writer

        self.driver = None
        self.html = None
        self.article_txid_list = None
        self.checked_article_txid_list = None
        self.obj_keyword = None  # keyword 검색 시, manytomany 에 추가 시켜줄 keyword 객체

    def crawl(self):

        html_s = time.time()
        self.get_html()  # self.html 셋팅
        html_e = time.time()
        print('검색결과 페이지 크롤링 시간', html_e - html_s)

        # 검색어가 정확히 입력된다면 article, writer, keyword 저장 후 True
        if self.html:  # 검색결과가 존재한다면
            self.get_article_txid_for_detail()  # 각 글들의 정보(아티클 링크)를 크롤링 한 뒤

            # request 수 제한을 위해 최신글 5개만 크롤링하도록 임의로 설정
            self.article_txid_list = self.article_txid_list[:5]

            self.check_duplicate()  # 중복검사를 통해 이미 저장한 아티클은 제외한다.

            # 예전 글을 포함하여 업데이트 하기위한 임의 설정
            # self.article_txid_list = self.article_txid_list[:5]

            self.crawl_detail_and_save()  # 상세페이지의 내용을 크롤링한다.

            return True

        else:  # 검색결과가 없는 경우 False
            return False

    # 검색 결과 목록을 크롤링
    def get_html(self):
        self.driver = set_headless_driver()  # 셀레니움 드라이버 셋팅

        try:
            if self.keyword:  # 키워드로 검색할 때는 최신순으로 정렬된 페이지를 크롤링
                url = f'https://brunch.co.kr/search?q={self.keyword}'
                self.driver.get(url)
                time.sleep(2)
                self.driver.find_elements_by_css_selector('span.search_option > a')[1].click()  # 최신순 정렬 클릭
                time.sleep(1)  # 최신순으로 누르고 기다리는 시간

            elif self.user_id:  # 작가의 글 페이지를 크롤링
                url = f'https://brunch.co.kr/@{self.user_id}#articles'
                self.driver.get(url)
                self.driver.find_element_by_css_selector('div.wrap_article_list')
            html = self.driver.page_source

        except (NoSuchElementException, ElementNotVisibleException):
            html = ''  # find_element 실패 시 Exception -> empty 'html'

        self.driver.close()
        self.html = html

    # 글 상세 페이지로 넘어갈 때 사용할 article_txid(아이디+글번호)를 리스트로 담아 리턴
    def get_article_txid_for_detail(self):
        soup = BeautifulSoup(self.html, 'lxml')
        li_article = soup.select('div.wrap_article_list > ul > li')

        article_txid_list = []
        for li in li_article:
            article_txid = li['data-articleuid']
            article_txid_list.append(article_txid)

        self.article_txid_list = article_txid_list

    def check_duplicate(self):
        # 중복 체크 후 새로 추가할 리스트
        checked_article_txid_list = [checked_article_txid for checked_article_txid in self.article_txid_list]
        # 이미 데이터에 존재하는 아티클

        for article_txid in self.article_txid_list:
            obj_article = Article.objects.filter(article_txid=article_txid)
            # 만약 존재하는 아티클이라면
            if obj_article:
                # 크롤링 할 리스트에서 제외해주고
                checked_article_txid_list.remove(article_txid)

        self.checked_article_txid_list = checked_article_txid_list

        # 키워드 검색일 경우 키워드를 저장
        if self.keyword:
            existed_article_txid = set(self.article_txid_list) - set(self.checked_article_txid_list)
            existed_article = [Article.objects.get(article_txid=article_txid) for article_txid in existed_article_txid]
            self.obj_keyword, _ = Keyword.objects.get_or_create(keyword=self.keyword)

            for article in existed_article:
                # 이미 존재하는 아티클에 키워드가 추가되어있지 않다면 키워드를 추가한다.
                if not article.keyword.filter(keyword=self.keyword):
                    article.keyword.add(self.obj_keyword)
                    article.save()

    # 상세페이지로 보내는 요청을 비동기적으로 구현
    # 각각의 상세페이지에서 아티클 정보 저장
    def crawl_detail_and_save(self):
        async def detail_crawl(url, article_txid):
            print(f'Send request .. {url}')

            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as res:
                    r = await res.text()
            soup = BeautifulSoup(r, 'lxml')

            print(f'Get response .. {url}')

            title = soup.find('meta', {'property': 'og:title'})['content']
            content = soup.select_one('div.wrap_body').prettify()
            media_name = soup.find('meta', {'name': 'article:media_name'})['content']

            try:  # 구독자 수 크롤링
                num_subscription = int(''.join(re.findall(
                    r'\w',
                    soup.select_one('span.num_subscription').text
                )))

            # 브런치에서 구독자 수가 1만을 초과하는 경우 '4.3만' 과 같이 표기된다.
            # 이때 int 형변환 시 '.' 과 '만' 때문에 ValueError 발생하므로 적절한 예외 처리 필요
            #   - '만' 을 '0000'으로 replace
            #   - 소수점 밑자리 숫자는 생략 처리
            except ValueError:
                char_num_subscription = soup.select_one('span.num_subscription').text
                trunc_part = ''.join(re.findall(r'.\d+', char_num_subscription))
                num_subscription = int(char_num_subscription.replace('만', '0000').replace(trunc_part, ''))

            published_time = re.findall(
                r'(\S+)\+',
                soup.find('meta', {'property': 'article:published_time'})['content'],
            )[0]
            user_id, text_id = re.findall(
                r'/@(\S+)/(\d+)',
                soup.find('meta', {'property': 'og:url'})['content']
            )[0]

            writer, _ = Writer.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'media_name': media_name,
                    'num_subscription': num_subscription
                }
            )

            # article 생성
            article_without_keyword = Article.objects.create(
                title=title,
                content=content,
                article_txid=article_txid,
                published_time=published_time,
                text_id=text_id,
                writer=writer
            )

            # article 에 keyword 추가(ManyToMany) - keyword 검색일 경우에 한하여
            if self.keyword:
                article_without_keyword.keyword.add(self.obj_keyword)

            print(f'저장 완료 {url}')

        # futures 에 Task 할당(url, 중복검사 완료된 checked_article_txid)
        async def create_task_async():
            brunch_url = 'https://brunch.co.kr/'

            # article_txid 문자열 변환을 통해 url 링크 생성(detail_crawl 의 인자가 됨)
            futures = [asyncio.ensure_future(
                detail_crawl(
                    brunch_url + '@@' + checked_article.replace('_', '/'), checked_article
                )
            )
                for checked_article in self.checked_article_txid_list]

            await asyncio.gather(*futures)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(create_task_async())

