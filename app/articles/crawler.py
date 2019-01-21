import asyncio
import re

import aiohttp
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from .models import Keyword, Article, Writer
from config.settings import BASE_DIR


class Crawler:
    def __init__(self, keyword=None, writer=None):
        self.keyword = keyword
        self.user_id = writer

        self.result = self.crawl()  # True or False 로 크롤링 결과 리턴

        self.driver = None
        self.html = None
        self.article_txid_list = None
        self.checked_article_txid_list = None
        self.obj_keyword = None  # keyword 검색 시, manytomany 에 추가 시켜줄 keyword 객체

    def crawl(self):
        self.get_html()  # self.html 셋팅

        # 검색어가 정확히 입력된다면 article, writer, keyword 저장 후 True
        if self.html:  # 검색결과가 존재한다면
            self.get_article_txid_for_detail()  # 각 글들의 정보(아티클 링크)를 크롤링 한 뒤

            # request 요청 제한을 위해 한번에 최대 5개만 크롤링하도록 임의로 설정
            # 여기에 제한을 두면 최신 글만 계속 업데이트 된다
            self.article_txid_list = self.article_txid_list[:5]

            self.check_duplicate()  # 중복검사를 통해 이미 저장한 아티클은 제외한다.

            # # 여기에 제한을 두면 예전 글과 최신글이 동시에 계속 업데이트 된다
            # self.article_txid_list = self.article_txid_list[:5]

            self.crawl_detail_and_save()  # 상세페이지의 내용을 크롤링한다.
            return True

        else:  # 검색결과가 없는 경우 False
            return False

    # 검색 결과 목록을 크롤링
    def get_html(self):
        self.set_headless_driver()  # 셀레니움 드라이버 셋팅

        try:
            if self.keyword:  # 키워드로 검색할 때는 최신순으로 정렬된 페이지를 크롤링
                url = f'https://brunch.co.kr/search?q={self.keyword}'
                self.driver.get(url)
                time.sleep(2)
                self.driver.find_elements_by_css_selector('span.search_option > a')[1].click()  # 최신순 정렬 클릭
                time.sleep(2)  # 최신순으로 누르고 기다리는 시간

            elif self.user_id:  # 작가의 글 페이지를 크롤링
                url = f'https://brunch.co.kr/@{self.user_id}#articles'
                self.driver.get(url)
                time.sleep(1)
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
        s = time.time()

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
            # article_uid = soup.find()
            num_subscription = int(''.join(re.findall(
                r'\w',
                soup.select_one('span.num_subscription').text
            )))
            published_time = re.findall(
                r'(\S+)\+',
                soup.find('meta', {'property': 'article:published_time'})['content'],
            )[0]
            user_id, text_id = re.findall(
                r'/@(\S+)/(\d+)',
                soup.find('meta', {'property': 'og:url'})['content']
            )[0]

            # writer(obj) 생성 및 할당
            writer, _ = Writer.objects.get_or_create(
                user_id=user_id,
                media_name=media_name,
                num_subscription=num_subscription,

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

        e = time.time()
        print('상세페이지 크롤링 시간', e - s)

    # Headless Chrome 으로 selenium driver 설정
    def set_headless_driver(self):
        chrome_driver_path = f'{os.path.join(os.path.join(BASE_DIR))}/chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920x1080')
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

        self.driver = driver
