from django.db import models


class Keyword(models.Model):
    search_word = models.CharField(verbose_name='검색 단어', null=False, max_length=200)


class Article(models.Model):
    title = models.CharField(verbose_name='제목', null=False, max_length=200)
    content = models.TextField(verbose_name='본문', null=False)
    keyword = models.ManyToManyField(Keyword, related_name='article')
    href = models.CharField(verbose_name='링크 조각', null=False, unique=True, max_length=200)
