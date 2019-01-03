from django.shortcuts import render

from articles.models import Article
from members.models import User


def index(request):
    user_all = User.objects.all()
    article_all = Article.objects.all()
    context = {
        'my_name': 'doh',
        'user_all': user_all,
        'article_all': article_all
    }

    return render(request, 'index.html', context=context)


