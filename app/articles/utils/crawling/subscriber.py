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


from requests_html import HTMLSession
if __name__ == '__main__':
    url = 'https://brunch.co.kr/@seungdols/following'
    session = HTMLSession()
    r = session.get(url)
    a = r.html.html.count('tit_subject')
    r.html.render(scrolldown=10)
    b = r.html.html.count('tit_subject')


    pass
