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
    # input_word_option 에는 'keyword' or 'user_id' 둘중 하나가 들어오도록 설정
    input_word_option = request.GET.get('input_word_option')
    input_word = request.GET.get("input_word")  # 검색어에 해당

    # Create Feed URL
    if input_word:
        # Create Crawler instance
        crawler = Crawler(
            keyword=input_word if input_word_option == 'keyword' else None,
            writer_id=input_word if input_word_option == 'writer' else None,
            user_id=input_word if input_word_option == 'user' else None,
        )

        # No crawling about option 'keyword' and 'writer'(it will be crawled when requests Feed url)
        # Execute crawling about option 'user'(it's not gonna be crawled when requests Feed url)
        if input_word_option == 'user':
            crawler.crawl()
        else:
            crawler.search_input_word()

        # crawler.html returns T/F about the result of searching brunch website
        if crawler.html:
            root_url = 'http://idontknow.kr/'
            feed_uri = f'feeds/{input_word_option}/{input_word}/'

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
                f'{"키워드" if input_word_option == "keyword" else "작가"} {input_word} 에 대한 검색결과 없음'
            )

    return redirect('articles:index')
