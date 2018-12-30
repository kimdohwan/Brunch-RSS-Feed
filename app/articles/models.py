from django.db import models


# Create your models here.

class Article(models.Model):
    uid = models.CharField(max_length=100)
    article_no = models.IntegerField()
    content = models.TextField()
