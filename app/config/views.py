from django.http import HttpResponse
from django.shortcuts import render

from articles.models import Article
from members.models import User


def index(request):
    u = User.objects.all()
    a = Article.objects.all()
    context = {
        'my_name': 'doh',
        'u': u,
        'a': a,
    }

    return render(request, 'index.html', context=context)
    # return HttpResponse('안녕')
