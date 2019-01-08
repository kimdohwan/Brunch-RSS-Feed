from django.urls import path

# from .feed.keyword import KeywordFeed
# from .feed.writer import WriterFeed
from .feed import KeywordFeed, WriterFeed
from .views import article_detail, index

app_name = 'articles'
urlpatterns = [
    path('', index, name='index'),
    path('detail/<pk>/', article_detail, name='article-detail'),
    path('feeds/keyword/<keyword>/', KeywordFeed(), name='feeds-keyword'),
    path('feeds/writer/<user_id>/', WriterFeed(), name='feeds-writer'),

]
