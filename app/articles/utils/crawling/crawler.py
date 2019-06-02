import asyncio
import re

import aiohttp
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from .driver import set_headless_driver
from ...models import Keyword, Article, Writer


class Crawler:
    def __init__(self, keyword=None, writer=None):
        self.keyword = keyword
        self.user_id = writer

        self.driver = None  # 크롤링에 사용할 selenium 드라이버
        self.html = None  # 검색결과 목록 페이지의 html
        self.article_txid_list = None  # 각각의 글들에 대한 id 를 담은 list
        self.cleand_txid_list = None  # DB에 존재하는 글을 '제외한' 글의 txid list

        self.obj_keyword = None  # keyword 검색 시, manytomany 에 추가 시켜줄 keyword 객체

    def crawl(self):

        html_s = time.time()
        self.get_search_result()  # self.html 셋팅
        html_e = time.time()
        print('검색결과 페이지 크롤링 시간', html_e - html_s)

        # 검색어가 정확히 입력된다면 article, writer, keyword 저장 후 True
        if self.html:  # 검색결과가 존재한다면
            self.get_article_txid()  # 글의 url 링크를 생성할 수 있는 txid(article id 에 해당)를 셋팅

            # request 수 제한을 위해 최신글 5개만 크롤링하도록 임의로 설정
            self.article_txid_list = self.article_txid_list[:3]

            self.remove_existed_article()  # 중복검사를 통해 이미 저장한 아티클은 제외한다.

            if self.keyword:  # Keyword 검색일 경우만 해당되는 처리(ManyToMany)
                self.set_keyword()

            self.crawl_detail_and_save()  # 상세페이지의 내용을 크롤링한 후 저장.

    @property
    def search_result(self):
        """
        크롤링 실행하기에 앞서, 검색결과의 존재 여부를 T/F 로 리턴
        """

        self.get_search_result()

        # html 이 셋팅되었다면 검색결과가 존재하며, None 이라면 검색결과 없음
        if self.html:
            return True
        return False

    def get_search_result(self):
        """
        javascript 로딩을 위해 selenium 드라이버 사용,
        검색결과가 존재 한다면 self.html 에 결과 페이지의 html source 할당
        """
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
                time.sleep(2)
                self.driver.find_element_by_css_selector('div.wrap_article_list')
            html = self.driver.page_source

        except (NoSuchElementException, ElementNotVisibleException):
            html = ''  # find_element 실패 시 Exception -> empty 'html'

        self.driver.close()
        self.html = html

    # 글 상세 페이지로 넘어갈 때 사용할 article_txid(아이디+글번호)를 리스트로 담아 리턴
    def get_article_txid(self):
        soup = BeautifulSoup(self.html, 'lxml')
        li_article = soup.select('div.wrap_article_list > ul > li')

        article_txid_list = []
        for li in li_article:
            article_txid = li['data-articleuid']
            article_txid_list.append(article_txid)

        self.article_txid_list = article_txid_list

    def remove_existed_article(self):
        """
        이미 존재하는 Article 인지 검사 후, 존재하는 Article 은 크롤링 목록에서 제거한다.
        제거한 목록을 self.clead_txid_list 값으로 셋팅한다.
        """

        cleand_txid_list = [txid for txid in self.article_txid_list]

        for article_txid in self.article_txid_list:
            try:
                obj = Article.objects.get(article_txid=article_txid)
            except Article.DoesNotExist:
                obj = None

            # 이미 존재하는 아티클이라면 크롤링 할 리스트에서 제외
            if obj:
                cleand_txid_list.remove(article_txid)

        self.cleand_txid_list = cleand_txid_list

    def set_keyword(self):
        """
        Keyword 검색에 해당하는 경우 실행되는 메서드.
        DB에 존재하는 Article 의 경우, 검색된 Keyword 를 추가.

        사례:
            상황: 'A'라는 글이 'python' 이라는 키워드로 크롤링 되어 이미 DB에 존재요청.
            -> 'django' 키워드로 검색 시 'A' 가 또 검색됨.
            -> 글 'A' 는 이미 DB에 존재하므로 'django'라는 Keyword 만 새로 추가해준다.
            결과: 글 'A' 는 'python', 'django' 라는 Keyword 를 Foreign Key 로 갖게 됨.
        """
        self.obj_keyword, _ = Keyword.objects.get_or_create(keyword=self.keyword)

        existed_article_txid = set(self.article_txid_list) - set(self.cleand_txid_list)
        existed_article = [Article.objects.get(article_txid=article_txid) for article_txid in existed_article_txid]

        for article in existed_article:
            # 이미 존재하는 아티클에 키워드가 추가되어있지 않다면 키워드를 추가한다.
            if not article.keyword.filter(keyword=self.keyword).exists():
                article.keyword.add(self.obj_keyword)
                article.save()

    def crawl_detail_and_save(self):
        """
        asyncio 모듈을 활용하여 비동기 를 통해 각각의 글(Article)들을 저장

        process:
            1. loop.run_until_complete : async loop 실행
            2. create_task_async() : 수행할 TASK 객체(detail_crawl() 수행) 생성
            3. detail_crawl() : Article 의 상세페이지 크롤링 및 저장
        """

        async def detail_crawl(url, article_txid):
            print(f'Send request .. {url}')

            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as res:
                    r = await res.text()  # 다음 TASK 를 실행하는 지점 / 응답이 온 순서대로 작업 실행하는 지점.
            soup = BeautifulSoup(r, 'lxml')

            print(f'Get response .. {url}')

            title = soup.find('meta', {'property': 'og:title'}).get('content')
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
            """
            TASK 객체를 생성한 후, gather() 을 통해 TASK(FUTURE) 전달 및 코루틴 실행
            """
            brunch_url = 'https://brunch.co.kr/'

            # article_txid 문자열 변환을 통해 url 링크 생성(detail_crawl 의 인자가 됨)
            futures = [
                asyncio.ensure_future(
                    detail_crawl(
                        url=brunch_url + '@@' + article_txid.replace('_', '/'),
                        article_txid=article_txid
                    )
                ) for article_txid in self.cleand_txid_list
            ]

            await asyncio.gather(*futures)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(create_task_async())
