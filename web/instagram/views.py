from django.shortcuts import render
# models
from instagram.models import Page


def index(request):
    return render(request, 'instagram/index.html')


def page(request, page_name_slug):
    context = {}
    page = Page.objects.get(slug=page_name_slug)
    context['page'] = page
    return render(request, 'instagram/page.html', context)


def search_page(request):
    search_token = request.GET.get('search_box')
    context = {}
    context['search'] = True
    context['keyword'] = search_token
    return render(request, 'instagram/page.html', context)
