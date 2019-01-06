from django.contrib import admin

# Register your models here.
from .models import Article, Keyword, Writer

admin.site.register(Article)
admin.site.register(Keyword)
admin.site.register(Writer)
