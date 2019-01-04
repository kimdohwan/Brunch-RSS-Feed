import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException

from articles.models import Article, Keyword
from config.settings import BASE_DIR


# 검색한 키워드를 인자로 받아 검색결과 html 페이지를 생성
def crawl(keyword):
    html = crawl_html(keyword)

    if html:
        href_list = get_href_to_detail(html)
        save_article(href_list, keyword)
    else:
        return '검색 결과 없음'


# selenium 으로 html 문자열을 리턴(selenium 코드는 여기만 해당됨)
def crawl_html(word):
    search_word = word

    chrome_driver_path = f'{os.path.join(os.path.join(BASE_DIR))}/chromedriver'
    driver = webdriver.Chrome(chrome_driver_path)

    url = f'https://brunch.co.kr/search?q={search_word}'
    driver.get(url)
    time.sleep(2)

    html = ''
    try:
        driver.find_elements_by_css_selector('span.search_option > a')[1].click()  # 최신순 정렬 클릭
        time.sleep(2)
        html = driver.page_source
    except ElementNotVisibleException:  # try: find_element 가 없을 때
        pass
    driver.close()
    return html


# 포스트 페이지로 넘어가는 링크(아이디+글번호)를 리스트에 담에 리턴
def get_href_to_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    li_article = soup.select('div.wrap_article_list > ul > li')

    href_list = []
    for li in li_article:
        a = li.find('a', href=True)
        href_list.append(a['href'])

    return href_list


# 본문내용과 제목을 포스트에 저장
# 이 함수에 너무 많은 기능을 넣은건가?
# - 데이터 중복검사
# - 상세페이지 크롤링
# - 데이터 저장
def save_article(href_list, keyword):
    href_list = href_list[:3]  # 테스트용, 3개만 긁자.

    obj_keyword, created = Keyword.objects.get_or_create(search_word=keyword)
    new_href_list = [new_href for new_href in href_list]

    # 이미 존재(저장되어있는)하는 포스트라면 항목 제거
    for href in href_list:
        obj_article = Article.objects.filter(href=href)
        if obj_article:
            new_href_list.remove(href)
            # 포스트가 현재 검색된 키워드를 가지지 않았다면 키워드는 추가시켜준다
            if not obj_article[0].keyword.filter(search_word=keyword):
                obj_article[0].keyword.add(obj_keyword)
                obj_article[0].save()

    # 해당 포스트 페이지 방문 후 크롤링 및 저장
    brunch_url = 'https://brunch.co.kr'
    for href in new_href_list:
        url = brunch_url + href
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.select_one('div.cover_cell').text
        content = soup.select_one('div.wrap_body').prettify()

        article_without_keyword = Article.objects.create(title=title, content=content, href=href)
        article_without_keyword.keyword.add(obj_keyword)
