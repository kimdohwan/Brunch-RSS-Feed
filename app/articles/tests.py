from django.test import TestCase
import asyncio

from articles.crawl import crawl
# crawl('아')
# save_article()

import time


async def sleep():
    await asyncio.sleep(2)


start = time.time()
# 이벤트 루프 정의
loop = asyncio.get_event_loop()
# 이벤트 루프 실행
loop.run_until_complete(sleep())
end = time.time()

print(str(end - start) + 's')
