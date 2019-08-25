"""
Urls
"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^search$', views.search, name='search'),
    url(r'^account$', views.account, name='account'),
    url(r'^legal$', views.legal, name='legal'),
    url(r'^mysubstitutes', views.mysubstitutes, name='mysubstitutes'),
]
