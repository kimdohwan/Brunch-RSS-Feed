from django.contrib import admin

# Register your models here.
from articles.models import Article

admin.site.register(Article)
