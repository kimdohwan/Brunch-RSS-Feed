from django.urls import reverse

from .customizing import CustomFeed
from ..models import Writer


class WriterFeed(CustomFeed):
    title = ''
    brunch_title = "Brunch 작가: "
    link = "/feeds/writer/"
    description = "등록한 작가의 최신글들을 업데이트합니다"

    def items(self, user_id):
        # Writer 에 연결된(Foreign key) Article
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
