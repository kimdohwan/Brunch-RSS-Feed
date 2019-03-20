from calendar import timegm

from django.contrib import messages
from django.contrib.syndication.views import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.http import http_date

from ..crawler import Crawler


# 장고 피드를 상속받아 필요한 부분을 커스터마이징
class MyFeed(Feed):
    def __call__(self, request, *args, **kwargs):

        keyword = kwargs.get('keyword')
        user_id = kwargs.get('user_id')
        # 피드 생성을 위해 페이지 크롤링(crawler.py)
        crawler = Crawler(keyword=keyword, writer=user_id)

        if not crawler.result:  # 잘못된 검색어로인해 결과 없을 경우
            messages.add_message(
                request,
                messages.INFO,
                f'"{"키워드" if keyword else "작가"}" {keyword or user_id} 에 대한 검색결과 없음'
            )  # 메시지 담아서 메인페이지로 리다이렉트
            return redirect('articles:index')

        try:  # 피드 생성
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
