from django.test import TestCase
import asyncio

from articles.crawl import crawl

crawl('아')
# save_article()
