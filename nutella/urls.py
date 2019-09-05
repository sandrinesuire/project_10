"""nutella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from substitute import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^substitute/', include('substitute.urls')),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/(?P<redirect_to>[A-Za-z0-9_/]*)$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]
