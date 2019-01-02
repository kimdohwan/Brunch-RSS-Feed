from django.shortcuts import render

from articles.models import Post
from members.models import User


def index(request):
    user_all = User.objects.all()
    post_all = Post.objects.all()
    context = {
        'my_name': 'doh',
        'user_all': user_all,
        'post_all': post_all
    }

    return render(request, 'index.html', context=context)


