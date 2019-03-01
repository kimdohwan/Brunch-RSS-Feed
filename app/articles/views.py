from django.shortcuts import render, redirect

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


def search(request):
    # search_option 에는 'keyword' or 'user_id' 둘중 하나가 들어오도록 설정
    search_option = request.GET.get('search')
    search_text = request.GET.get("search_text")  # 검색어에 해당

    if search_text:
        return redirect(f'articles:feeds-{search_option}', search_text)
    return redirect('articles:index')
