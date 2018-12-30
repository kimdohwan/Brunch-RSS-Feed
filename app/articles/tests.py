from django.test import TestCase
import asyncio

from articles.views import test_crawl

# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_crawl())
# loop.close

test_crawl()