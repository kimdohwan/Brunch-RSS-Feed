from django.urls import reverse

from .customizing import CustomFeed
from ..models import Keyword


# django Feed 를 사용, get_object() 함수로 검색어를 items() 에 전달
class KewordFeed(CustomFeed):
    title = ''
    brunch_title = "Brunch 키워드: "
    link = "/feeds/keyword/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self, keyword):
        # Keword 에 연결된(ManyToMany) Article
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
        # self.title 은 Feed 의 title
        # item_title 은 각각의 article 의 title
        self.title = self.brunch_title + kwargs["keyword"]
        return str(kwargs['keyword'])
