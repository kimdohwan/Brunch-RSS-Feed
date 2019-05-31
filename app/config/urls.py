from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('articles.urls')),
    path('admin/', admin.site.urls),
]


def trigger_error(request):
    # error_val = 1/0
    return None


urlpatterns += [
    path('sentry/', trigger_error)
]