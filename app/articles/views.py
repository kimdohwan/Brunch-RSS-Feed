import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException

from articles.models import Posts
from config.settings import BASE_DIR


# 검색한 키워드를 인자로 받아 검색결과 html 페이지를 생성
def crawl(word):
    html = crawl_html(word)

    if html:
        href_list = get_href_to_detail(html)
        save_article(href_list)
    else:
        print('검색 결과 없음')


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
        driver.find_elements_by_css_selector('span.search_option > a')[1].click()
        time.sleep(3)
        html = driver.page_source
    except ElementNotVisibleException:
        pass
    driver.close()
    return html


# 포스트 페이지로 넘어가는 링크를 리스트에 담에 리턴
def get_href_to_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    li_article = soup.select('div.wrap_article_list > ul > li')

    href_list = []
    for li in li_article:
        a = li.find('a', href=True)
        href_list.append(a['href'])

    return href_list


# 본문내용과 제목을 포스트에 저장
def save_article(href_list):
    brunch_url = 'https://brunch.co.kr'
    article_url_list = [brunch_url + href for href in href_list]
    n = 0
    for url in article_url_list:
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.select_one('div.cover_cell').text
        content = soup.select_one('div.wrap_body').prettify()

        Posts.objects.create(name=title, content=content)

