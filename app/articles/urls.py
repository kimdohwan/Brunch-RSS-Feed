from django.urls import path

from articles.feed import TestFeed, article_detail

urlpatterns = [
    path('<pk>/', article_detail, name='article-detail'),
    path('feeds/<keyword>/', TestFeed(), name='feeds')
]
