from django.contrib import admin

# Register your models here.
from members.models import User

admin.site.register(User)
