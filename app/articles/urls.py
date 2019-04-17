from django.urls import path

from articles.tests import test
from .feeds import KeywordFeed, WriterFeed, UserFeed
from .views import article_detail, index, create_feed_url

app_name = 'articles'
urlpatterns = [
    path('', index, name='index'),
    path('create_feed_url/', create_feed_url, name='create_feed_url'),
    path('detail/<pk>/', article_detail, name='article-detail'),
    path('feeds/keyword/<keyword>/', KeywordFeed(), name='feeds-keyword'),
    path('feeds/writer/<writer_id>/', WriterFeed(), name='feeds-writer'),
    path('feeds/user/<user_id>/', UserFeed(), name='feeds-user'),
    path('test/<keyword>/', test),
]
