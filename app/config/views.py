from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {
        'my_name': 'doh'
    }
    return render(request, 'index.html', context=context)
    # return HttpResponse('안녕')
