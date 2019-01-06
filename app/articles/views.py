from django.shortcuts import render, redirect

from .crawl import crawl
from .models import Article, Keyword, Writer


# Feed 생성에 필요한 article detail view
def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'article-detail.html', context=context)


# index view 에서 하는 역할
# - 검색어(search_text) 를 받는다
# - 작가/키워드 여부에 따라 크롤링 실시 -> Feed url 로 redirect
# - 크롤링이 실패하면 no result alert 을 띄워준다
def index(request):
    k, w = ('keyword', 'writer')

    search_option = request.GET.get('search')
    search_text = request.GET.get("search_text")
    context = dict()

    # 검색어가 주어졌을 때의 처리
    # crawl() 은 성공 시 True, 실패 시 False 를 return
    if search_text:
        if search_option == k:
            result = crawl(keyword=search_text)
            if result:  # keword feed 생성 및 redirect to Feed page
                return redirect(f'articles:feeds-{search_option}', keyword=search_text)
        elif search_option == w:
            result = crawl(writer=search_text)
            if result:  # writer feed 생성 및 redirect to Feed page
                return redirect(f'articles:feeds-{search_option}', user_id=search_text)

        context['no_result'] = search_text

    # 경우1: 검색어가 주어지지 않은 경우 - 기본 접속
    # 경우2: 검색어가 주어졌으나 크롤링 후 검색결과가 없는 경우 - alert 팝업(no_result)
    keywords = Keyword.objects.all()
    writers = Writer.objects.all()
    context['keywords'], context['writers'] = keywords, writers

    return render(request, 'index.html', context=context)
