from calendar import timegm

import requests
from django.contrib.syndication.views import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.utils.feedgenerator import DefaultFeed
from django.utils.http import http_date

from ..crawler import Crawler

class MyDefaultFeed(DefaultFeed):
    content_type = 'application/xml; charset=utf-8'


# 장고 피드를 상속받아 필요한 부분을 커스터마이징
class MyFeed(Feed):
    feed_type = MyDefaultFeed

    def __call__(self, request, *args, **kwargs):

        # url 로부터 parameter 를 셋팅
        keyword = kwargs.get('keyword')
        user_id = kwargs.get('user_id')

        # Django Crawler 사용 - crawler.py
        crawler = Crawler(keyword=keyword, writer=user_id)
        crawler.crawl()

        # # lambda crawler
        # requests.post(
        #     "https://7n82o95659.execute-api.ap-northeast-2.amazonaws.com/Post/",
        #     json={
        #         "keyword": keyword,
        #         "writer": user_id,
        #     })
        try:
            obj = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404('Feed object does not exist.')
        feedgen = self.get_feed(obj, request)
        response = HttpResponse(content_type=feedgen.content_type)
        if hasattr(self, 'item_pubdate') or hasattr(self, 'item_updateddate'):
            response['Last-Modified'] = http_date(
                timegm(feedgen.latest_post_date().utctimetuple()))
        feedgen.write(response, 'utf-8')
        return response

    def item_title(self, item):
        return item.title  # 포스팅의 제목 설정(피드 이름 아님)

    def item_description(self, item):
        return item.content  # 글 내용

    def item_pubdate(self, item):
        return item.published_time  # 글쓴 시간

    def item_link(self, item):  # 내 피드 페이지가 아닌 브런치 페이지로 이동
        return f'https://brunch.co.kr/@@{item.article_txid.replace("_", "/")}'

    def get_feed(self, obj, request):
        self.title = self.brunch_title + obj  # 피드의 이름 설정(포스팅 제목 아님)
        feed = super().get_feed(obj, request)
        return feed
