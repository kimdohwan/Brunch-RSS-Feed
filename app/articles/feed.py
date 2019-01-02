from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse
from django.utils.feedgenerator import SyndicationFeed, Rss201rev2Feed, rfc2822_date

from articles.models import Post


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post-detail.html', context=context)


class TestFeed(Feed):
    title = ''
    brunch_title = "Brunch Feed: "
    link = "/feeds/"
    description = "등록한 검색어의 최신글들을 업데이트합니다"

    def items(self, keyword):
        return Post.objects.filter(keyword=keyword)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])

    def get_object(self, request, *args, **kwargs):
        self.title = self.brunch_title + kwargs["keyword"]
        return str(kwargs['keyword'])
