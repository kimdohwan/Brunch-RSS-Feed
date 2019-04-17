from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from articles.crawler import Crawler
from .models import Article, Keyword, Writer


def index(request):
    keywords = Keyword.objects.all()
    writers = Writer.objects.all().order_by('-num_subscription')[:20]
    context = {
        'keywords': keywords,
        'writers': writers,
    }
    return render(request, 'index.html', context=context)


# article detail view
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'article-detail.html', context=context)


def create_feed_url(request):
    # input_option = 'keyword' or 'user_id'
    input_word = request.GET.get('input_word')
    input_option = request.GET.get("input_option")

    crawler = Crawler(
        keyword=input_option if input_option == 'keyword' else None,
        writer=input_word if input_option == 'writer' else None,
    )
    crawler.get_html()

    if crawler.html:
        root_url = 'http://idontknow.kr/'
        feed_uri = f'feeds/{input_option}/{input_word}/'

        # On runserver
        if settings.DEBUG:
            root_url = 'http://localhost:8000/'

        # django messages return Feed URL
        messages.add_message(
            request,
            messages.INFO,
            'Feed URL',
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            root_url + feed_uri,
        )

    # no result from user's 'input word'
    else:
        messages.add_message(
            request,
            messages.WARNING,
            f'{"키워드" if input_option == "keyword" else "작가"} {input_word} 에 대한 검색결과 없음'
        )

    return redirect('articles:index')