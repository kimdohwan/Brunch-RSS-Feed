import os

from pyppeteer import launch
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from requests_html import AsyncHTMLSession
from requests_html import HTMLSession


def test_crawl():
    file_path = f'{os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")}/a.html'
    search_word = '파이썬'
    url = f'https://brunch.co.kr/search?q={search_word}'
    # url = f'https://www.wadiz.kr/web/wreward/main?keyword=&endYn=ALL&order=recommend'

    r = HTMLSession().get(url)
    r.html.render(retries=100, scrolldown=1000, wait=3)

    # asession = AsyncHTMLSession()
    #
    # r = asession.get(url)
    # await r.html.arender()
    #
    # b = await launch()
    # page = await b.newPage()
    # await page.goto(url)
    # await page.screenshot({'path': 'p.png', 'fullPage': True})
    # await b.close()



    # r = requests.get(url)
    open(file_path, 'w').write(r.html.html)
    # print(a)
    # # f = open(file_path, 'rt').read()
    # #
    # # soup = BeautifulSoup(f, 'lxml')
    # # sub = soup.find_all('div')
    # # print(sub)

    # session = HTMLSession()
    # r = session.get(url)
    # r.html.render()
    # print(r.html.html)



    pass