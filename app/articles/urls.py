from django.urls import path

from .feed import TestFeed
from .views import search_keyword, article_detail

app_name = 'articles'
urlpatterns = [
    path('', search_keyword, name='search-keyword'),
    path('detail/<pk>/', article_detail, name='article-detail'),
    path('feeds/<keyword>/', TestFeed(), name='feeds'),
]
