from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse

from articles.models import Posts


def post_detail(request, pk):
    post = Posts.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post-detail.html', context=context)


class TestFeed(Feed):
    title = "브런치 검색어 피드"
    link = "/feeds/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self):
        return Posts.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])
