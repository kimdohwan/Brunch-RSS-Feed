import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException

from config.settings import BASE_DIR


# 검색한 키워드를 인자로 받아 검색결과 html 페이지를 생성
def crawl(word):
    html = crawl_html(word)

    if html:
        href_list = get_href_to_detail(html)
        save_article(href_list)
    else:
        print('검색 결과 없음')


def crawl_html(word):
    search_word = word

    chrome_driver_path = f'{os.path.join(os.path.join(BASE_DIR))}/chromedriver'
    driver = webdriver.Chrome(chrome_driver_path)

    url = f'https://brunch.co.kr/search?q={search_word}'
    driver.get(url)

    try:
        driver.find_elements_by_css_selector('span.search_option > a')[1].click()
        time.sleep(2)
        html = driver.page_source
        return html
    except ElementNotVisibleException:
        return


def get_href_to_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    li_article = soup.select('div.wrap_article_list > ul > li')

    href_list = []
    for li in li_article:
        a = li.find('a', href=True)
        href_list.append(a['href'])

    return href_list


def save_article(href_list):
    brunch_url = 'https://brunch.co.kr'
    article_url_list = [brunch_url + href for href in href_list]
    for i in article_url_list:
        print(i)
    pass

