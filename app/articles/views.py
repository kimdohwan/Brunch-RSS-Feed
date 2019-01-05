from django.shortcuts import render, redirect

from .crawl import *


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'article-detail.html', context=context)


def search_keyword(request):
    keyword = request.GET.get("keyword")
    context = dict()

    if keyword:
        result = crawl(f'{keyword}')
        if not result:
            context['no_result'] = keyword
        else:
            return redirect('articles:feeds', keyword=keyword)

    keywords = Keyword.objects.all()
    context['keywords'] = keywords
    return render(request, 'search_keyword.html', context=context)

