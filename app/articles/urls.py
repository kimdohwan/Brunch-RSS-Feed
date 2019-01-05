from django.urls import path

from .feed import KewordFeed, WriterFeed
from .views import search_keyword, article_detail

app_name = 'articles'
urlpatterns = [
    path('', search_keyword, name='search-keyword'),
    path('detail/<pk>/', article_detail, name='article-detail'),
    path('feeds/keyword/<keyword>/', KewordFeed(), name='feeds-keyword'),
    path('feeds/writer/<user_id>/', WriterFeed(), name='feeds-writer'),

]
