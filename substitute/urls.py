"""
Urls
"""

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^search$', views.search, name='search'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^account$', views.account, name='account'),
    url(r'^legal$', views.legal, name='legal'),
    url(r'^results', views.results, name='results'),
    url(r'^mysubstitutes', views.mysubstitutes, name='mysubstitutes'),
]
