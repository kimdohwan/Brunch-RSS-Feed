from django.urls import path

from articles.feed import TestFeed, post_detail

urlpatterns = [
    path('posts/<pk>/', post_detail, name='post-detail'),
    path('feeds/<keyword>/', TestFeed(), name='feeds')
]
