from celery import shared_task

from .models import Keyword
from .utils.crawling.crawler import Crawler
from config import celery_app


@shared_task
def task_for_crawling(keyword, writer):
    c = Crawler(keyword=keyword, writer=writer)
    c.crawl()


# @celery_app.task(name='test_beat')
# def test_beat():
#     query_set = Keyword.objects.all()
#     for q in query_set:
#         keyword = q.keyword
#         c = Crawler(keyword=keyword)
#         print(' - celery beat: ', keyword, '크롤링 시작')
#         c.crawl()
