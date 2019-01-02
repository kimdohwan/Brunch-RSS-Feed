from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(verbose_name='제목', null=False, max_length=100)
    content = models.CharField(verbose_name='본문', null=False, max_length=300)
    keyword = models.CharField(verbose_name='키워드', null=False, max_length=50)
