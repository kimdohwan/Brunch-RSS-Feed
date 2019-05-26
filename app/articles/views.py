from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from articles.tasks import task_for_crawling
from .utils.crawling.crawler import Crawler
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
    input_word = request.GET.get('input_word')  # 검색한 단어
    input_option = request.GET.get("input_option", "keyword")  # 검색 옵션(기본 설정: keyword)

    keyword = input_word if input_option == 'keyword' else None
    writer = input_word if input_option == 'writer' else None

    # 검색결과가 존재여부 검사를 위해 크롤러 객체 생성
    crawler = Crawler(keyword=keyword, writer=writer)

    # search_result 가 True 일 경우 검색 결과 존재
    if crawler.search_result:

        # 백그라운드에서 크롤링을 실행하게 됨
        task_for_crawling.delay(keyword=keyword, writer=writer)

        root_url = request.META['HTTP_REFERER']
        feed_uri = f'feeds/{input_option}/{input_word}/'

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
            f'{"키워드" if keyword else "작가"} {input_word} 에 대한 검색결과 없음'
        )

    return redirect('articles:index')
