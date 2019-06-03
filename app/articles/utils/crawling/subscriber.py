#
# from .crawler import Crawler
#
#
# class SubCrawler:
#     def __init__(self, subscriber=None):
#         self.user_id = subscriber
#
#         self.writer_list = None
#
#         self.driver = None
#
#     def load_javascript(self):
#         pass
#
#     def get_writer_list(self):
#         pass
#
#     def execute_crawler(self):
#         for writer in self.writer_list:
#             crawler = Crawler(writer=writer)
#             crawler.crawl()
#         pass


# from requests_html import HTMLSession
import time

from selenium.webdriver.common.keys import Keys

from articles.utils.crawling.driver import set_headless_driver

if __name__ == '__main__':
    url = 'https://brunch.co.kr/@annejeong/following'
    #     session = HTMLSession()
    #     r = session.get(url)
    #     a = r.html.html.count('tit_subject')
    #     r.html.render(scrolldown=10)
    #     b = r.html.html.count('tit_subject')
    #
    #
    #     pass

    driver = set_headless_driver()
    driver.get(url)
    body = driver.find_element_by_tag_name("body")
    SCROLL_PAUSE_TIME = 0.5
    for i in range(1,100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        n = driver.find_element_by_xpath('/html/body/main/div/div[1]/strong/span').text
        a = driver.page_source.count('tit_subject')
        b = driver.page_source.count('박창선')
        if n == a:
            break
    #
    # while True:
    #
    #     # Get scroll height
    #     ### This is the difference. Moving this *inside* the loop
    #     ### means that it checks if scrollTo is still scrolling
    #     last_height = driver.execute_script("return document.body.scrollHeight")
    #
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    #
    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #
    #         # try again (can be removed)
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #         # Wait to load page
    #         time.sleep(SCROLL_PAUSE_TIME)
    #
    #         # Calculate new scroll height and compare with last scroll height
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #
    #         # check if the page height has remained the same
    #         n = driver.find_element_by_xpath('/html/body/main/div/div[1]/strong/span').text
    #         a = driver.page_source.count('tit_subject')
    #         b = driver.page_source.count('정주홍')
    #         if n == a:
    #             break
    #         # if not, move on to the next loop
    #         else:
    #             last_height = new_height
    #             continue