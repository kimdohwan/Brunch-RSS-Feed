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
        self.href_list = None
        self.checked_href_list = None
        self.obj_keyword = None  # keyword 검색 시, manytomany 에 추가 시켜줄 keyword 객체

    def crawl(self):
        self.get_html()  # self.html 셋팅

        # 검색어가 정확히 입력된다면 article, writer, keyword 저장 후 True
        if self.html:
            self.get_href_for_detail()
            self.check_duplicate()
            self.crawl_detail_and_save()
            return True

        else:  # 검색결과가 없는 경우 False
            return False

    def get_html(self):
        self.set_headless_driver()

        try:
            # 키워드로 검색할 때는 최신순으로 정렬된 페이지를 크롤링
            if self.keyword:
                url = f'https://brunch.co.kr/search?q={self.keyword}'
                self.driver.get(url)
                time.sleep(1)
                self.driver.find_elements_by_css_selector('span.search_option > a')[1].click()  # 최신순 정렬 클릭
                time.sleep(1)  # 최신순으로 누르고 기다리는 시간
            # 작가의 글 페이지를 크롤링
            elif self.user_id:
                url = f'https://brunch.co.kr/@{self.user_id}#articles'
                self.driver.get(url)
                time.sleep(1)
                self.driver.find_element_by_css_selector('div.wrap_article_list')
            html = self.driver.page_source

        except (NoSuchElementException, ElementNotVisibleException):
            html = ''  # find_element 실패 시 Exception -> empty 'html'

        self.driver.close()
        self.html = html

    # 포스트 페이지로 넘어가는 링크(아이디+글번호)를 리스트에 담에 리턴
    def get_href_for_detail(self):
        soup = BeautifulSoup(self.html, 'lxml')
        li_article = soup.select('div.wrap_article_list > ul > li')

        href_list = []
        for li in li_article:
            a = li.select_one('li > a.link_post')
            href_list.append(a['href'])

        self.href_list = href_list

    def check_duplicate(self):
        # 중복 체크 후 새로 추가할 리스트
        checked_href_list = [checked_href for checked_href in self.href_list]
        # 이미 데이터에 존재하는 아티클

        for href in self.href_list:
            obj_article = Article.objects.filter(href=href)
            # 만약 존재하는 아티클이라면
            if obj_article:
                # 크롤링 할 리스트에서 제외해주고
                checked_href_list.remove(href)

        self.checked_href_list = checked_href_list

        # 키워드 검색일 경우 키워드를 저장
        if self.keyword:
            existed_href = set(self.href_list) - set(self.checked_href_list)
            existed_article = [Article.objects.get(href=href) for href in existed_href]
            self.obj_keyword, _ = Keyword.objects.get_or_create(keyword=self.keyword)

            for article in existed_article:
                # 이미 존재하는 아티클에 키워드가 추가되어있지 않다면 키워드를 추가한다.
                if not article.keyword.filter(keyword=self.keyword):
                    article.keyword.add(self.obj_keyword)
                    article.save()

    def crawl_detail_and_save(self):
        s = time.time()

        # ---------비동기화(asyncio) X--------------------------------------
        # brunch_url = 'https://brunch.co.kr'
        # for href in new_href_list:
        #     url = brunch_url + href
        #     r = requests.get(url)
        #     soup = BeautifulSoup(r.text, 'lxml')
        # ----------------------------------------------------------------

        # ---------비동기화(asyncio) O--------------------------------------
        async def detail_crawl(url, new_href):
            print(f'Send request .. {url}')

            # ----------requests module 이용-------------
            # loop = asyncio.get_event_loop()
            # r = await loop.run_in_executor(None, requests.get, url)
            # soup = BeautifulSoup(r.text, 'lxml')
            # ------------------------------------------

            # -----------aiohttp module 이용-------------
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as res:
                    r = await res.text()
            soup = BeautifulSoup(r, 'lxml')
            # ------------------------------------------

            print(f'Get response .. {url}')

            title = soup.select_one('div.cover_cell').text
            content = soup.select_one('div.wrap_body').prettify()
            media_name = soup.find('meta', {'name': 'article:media_name'})['content']
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
                media_name=media_name
            )

            # article 생성
            article_without_keyword = Article.objects.create(
                title=title,
                content=content,
                href=new_href,
                published_time=published_time,
                text_id=text_id,
                writer=writer
            )

            # article 에 keyword 추가(ManyToMany)
            if self.keyword:
                article_without_keyword.keyword.add(self.obj_keyword)

            print(f'저장 완료 {url}')

        # futures 에 Task 할당(url, 중복검사 완료된 href(new_href))
        async def create_task_async():
            brunch_url = 'https://brunch.co.kr'
            futures = [asyncio.ensure_future(
                detail_crawl(
                    brunch_url + new_href, new_href
                )
            )
                for new_href in self.checked_href_list]

            await asyncio.gather(*futures)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(create_task_async())
        # ----------------------------------------------------------------

        e = time.time()
        print('상세페이지 크롤링 시간', e - s)

    def set_headless_driver(self):
        chrome_driver_path = f'{os.path.join(os.path.join(BASE_DIR))}/chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

        self.driver = driver
