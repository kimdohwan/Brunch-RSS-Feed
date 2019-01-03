from django.contrib.syndication.views import Feed
from django.shortcuts import render, redirect
from django.urls import reverse

from articles.customize_feed import CustomFeed
from articles.models import Article, Keyword


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'article-detail.html', context=context)


# django Feed 를 사용, get_object() 함수로 검색어를 items 에 전달
class TestFeed(CustomFeed):
    title = ''
    brunch_title = "Brunch Feed: "
    link = "/feeds/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self, keyword):
        return Keyword.objects.get(search_word=keyword).article.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('article-detail', args=[item.pk])

    def get_object(self, request, *args, **kwargs):
        self.title = self.brunch_title + kwargs["keyword"]
        return str(kwargs['keyword'])
