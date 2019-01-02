from django.contrib import admin

# Register your models here.
from articles.models import Post

admin.site.register(Post)
