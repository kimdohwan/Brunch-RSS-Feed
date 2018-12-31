from django.db import models


# Create your models here.

class Article(models.Model):
    uid = models.CharField(max_length=100)
    article_no = models.IntegerField()
    content = models.TextField()


class Posts(models.Model):
    name = models.CharField(verbose_name='Name', null=False, max_length=50)
    content = models.CharField(verbose_name='Content', null=False, max_length=300)
