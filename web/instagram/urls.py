#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: darkodivjakovski
"""

from django.conf.urls import url
from instagram import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^page/(?P<page_name_slug>[\w\-._#%^$&!/]+)/$', views.page, name='instagram-page'),
    url(r'^search/$',views.search_page),
]
