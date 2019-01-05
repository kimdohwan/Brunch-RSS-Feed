from django.shortcuts import render, redirect

from articles.models import Article, Keyword
from .crawl import *


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'article-detail.html', context=context)


def search_keyword(request):
    option = request.GET.get('search')
    search_text = request.GET.get("search_text")
    context = dict()

    if search_text:
        if option == 'keyword':
            result = crawl(keyword=search_text, k=10)
            if result:
                return redirect(f'articles:feeds-{option}', keyword=search_text)
            else:
                context['no_result'] = search_text

        elif option == 'writer':
            result = crawl(writer=search_text, k=10)
            if result:
                return redirect(f'articles:feeds-{option}', user_id=search_text)
            else:
                context['no_result'] = search_text

    keywords = Keyword.objects.all()
    writers = Writer.objects.all()
    context['keywords'], context['writers'] = keywords, writers

    return render(request, 'search_keyword.html', context=context)
