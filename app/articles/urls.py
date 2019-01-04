from django.urls import path

from articles.feed import TestFeed, article_detail
from articles.views import search_keyword

app_name = 'articles'
urlpatterns = [
    path('detail/<pk>/', article_detail, name='article-detail'),
    path('', search_keyword, name='search-keyword'),
    path('feeds/<keyword>/', TestFeed(), name='feeds')
]
