from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse('안녕')
    context = {
        'my_name': 'doh'
    }
    return render(request, 'index.html', context=context)
