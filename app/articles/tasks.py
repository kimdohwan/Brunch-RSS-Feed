from celery import shared_task

from .utils.crawling.crawler import Crawler


@shared_task
def task_for_crawling(keyword, writer):
    c = Crawler(keyword=keyword, writer=writer)
    c.crawl()
