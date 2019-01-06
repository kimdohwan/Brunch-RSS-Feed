import os
import asyncio
import re
import time
import aiohttp
import requests
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from bs4 import BeautifulSoup

from .models import Article, Keyword, Writer
from config.settings import BASE_DIR


# 검색한 키워드를 인자로 받아 검색결과 html 페이지를 생성
def crawl(keyword=None, writer=None):
    html = get_html(keyword, writer)

    # 검색어가 정확히 입력된다면 article, writer, keyword 저장 후 True
    if html:
        href_list = get_href_for_detail(html)
        # save_article 에서 writer id 를 href 를 통해 얻기때문에 keyword 만 전달
        save_article(href_list, keyword)
        return True

    # 검색결과가 없는 경우 False
    else:
        return False


# selenium 으로 html 문자열을 리턴(selenium 코드는 여기만 해당됨)
def get_html(keyword=None, writer=None):
    # headless chrome driver 설정
    chrome_driver_path = f'{os.path.join(os.path.join(BASE_DIR))}/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

    try:
        # 키워드로 검색할 때는 최신순으로 정렬된 페이지를 크롤링
        if keyword:
            url = f'https://brunch.co.kr/search?q={keyword}'
            driver.get(url)
            time.sleep(2)
            driver.find_elements_by_css_selector('span.search_option > a')[1].click()  # 최신순 정렬 클릭
            time.sleep(2)  # 최신순으로 누르고 기다리는 시간
        # 작가의 글 페이지를 크롤링
        elif writer:
            url = f'https://brunch.co.kr/@{writer}#articles'
            driver.get(url)
            time.sleep(2)
            driver.find_element_by_css_selector('div.wrap_article_list')
        html = driver.page_source

    # find_element 실패 시 Exception -> empty 'html'
    except (NoSuchElementException, ElementNotVisibleException):
        html = ''

    driver.close()
    return html


# 포스트 페이지로 넘어가는 링크(아이디+글번호)를 리스트에 담에 리턴
def get_href_for_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    li_article = soup.select('div.wrap_article_list > ul > li')

    href_list = []
    for li in li_article:
        a = li.select_one('li > a.link_post')
        href_list.append(a['href'])

    return href_list


# 본문내용과 제목을 포스트에 저장
# 이 함수에 너무 많은 기능을 넣은건가?
# - 데이터 중복검사
# - 상세페이지 크롤링
# - 데이터 저장
def save_article(href_list, keyword=None):
    href_list = href_list[:3]  # 테스트용, 3개만 긁자.

    obj_keyword, created = Keyword.objects.get_or_create(keyword=keyword)
    new_href_list = [new_href for new_href in href_list]

    # 이미 존재(저장되어있는)하는 포스트라면 항목 제거
    for href in href_list:
        obj_article = Article.objects.filter(href=href)
        if obj_article:
            new_href_list.remove(href)
            # 포스트가 현재 검색된 키워드를 가지지 않았다면 키워드는 추가시켜준다
            if not obj_article[0].keyword.filter(keyword=keyword):
                obj_article[0].keyword.add(obj_keyword)
                obj_article[0].save()

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
        article_without_keyword.keyword.add(obj_keyword)

        print(f'저장 완료 {url}')

    # futures 에 Task 할당(url, 중복검사 완료된 href(new_href))
    async def create_task_async():
        brunch_url = 'https://brunch.co.kr'
        futures = [asyncio.ensure_future(
            detail_crawl(
                brunch_url + new_href, new_href
            )
        )
            for new_href in new_href_list]

        await asyncio.gather(*futures)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_task_async())
    # ----------------------------------------------------------------

    e = time.time()
    print('상세페이지 크롤링 시간', e - s)
