"""openbar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'openbar.main.index'),
    url(r'^show_login/$', 'openbar_users.views.login_page', name='show_login'),
    url(r'^login$', 'openbar_users.views.app_login', name='login'),
    url(r'^logout$', 'openbar_users.views.app_logout', name='logout'),
    url(r'^create_account/$', 'openbar_users.views.create_account', name='create_account'),
    url(r'^searcher/new/$', 'openbar_users.views.create_searcher', name='new_searcher'),
]
