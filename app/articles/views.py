from django.http import HttpResponse
from django.shortcuts import render, redirect

from .crawl import *


def search_keyword(request):
    if request.method == 'POST':
        keyword = request.POST["keyword"]
        check_keyword = request.POST["check_keyword"]
        if keyword == check_keyword:
            crawl(f'{keyword}')
            return redirect('articles:feeds', keyword=keyword)
        else:
            context = {
                'keyword': keyword,
                'after_search': f'검색어 "{keyword}" 에 대한 피드를 생성합니다(검색어를 한번 더 입력해주세요)',
                'not_matched': f'틀린 검색어어입니다. 입력한 검색어: "{check_keyword}"',
            }
    else:
        keyword = request.GET.get('keyword')
        if keyword:
            context = {
                'keyword': keyword,
                'after_search': f'검색어 "{keyword}" 에 대한 피드를 생성합니다(검색어를 한번 더 입력해주세요)',
            }
        else:
            return render(request, 'search_keyword.html')

    return render(request, 'search_keyword.html', context=context)
