from django.test import TestCase
import asyncio

from articles.views import crawl, save_article

crawl('크롤링')
# save_article()
