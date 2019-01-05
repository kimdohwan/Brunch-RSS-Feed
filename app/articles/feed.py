from django.urls import reverse

from .customize_feed import CustomFeed
from .models import Keyword, Writer


# django Feed 를 사용, get_object() 함수로 검색어를 items 에 전달
class KewordFeed(CustomFeed):
    title = ''
    brunch_title = "Brunch Feed: "
    link = "/feeds/keyword/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self, keyword):
        return Keyword.objects.get(keyword=keyword).articles.all().order_by('-published_time')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.published_time

    def item_link(self, item):
        return reverse('article-detail', args=[item.pk])

    def get_object(self, request, *args, **kwargs):
        self.title = self.brunch_title + kwargs["keyword"]
        return str(kwargs['keyword'])


class WriterFeed(CustomFeed):
    title = ''
    brunch_title = "Brunch Feed: "
    link = "/feeds/writer/"
    description = "등록한 작가의 최신글들을 업데이트합니다"

    def items(self, user_id):
        return Writer.objects.get(user_id=user_id).articles.all().order_by('-published_time')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.published_time

    def item_link(self, item):
        return reverse('article-detail', args=[item.pk])

    def get_object(self, request, *args, **kwargs):
        self.title = self.brunch_title + kwargs["user_id"]
        return str(kwargs['user_id'])
