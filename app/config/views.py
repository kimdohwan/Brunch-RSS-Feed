from django.shortcuts import render

from articles.models import Article, Posts
from members.models import User


def index(request):
    user_all = User.objects.all()
    article_all = Article.objects.all()
    post_all = Posts.objects.all()
    context = {
        'my_name': 'doh',
        'user_all': user_all,
        'article_all': article_all,
        'post_all': post_all
    }

    return render(request, 'index.html', context=context)


