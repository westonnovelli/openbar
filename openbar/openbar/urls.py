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
    url(r'^$', 'openbar.main.index', name='index'),

    url(r'^animate$', 'openbar.main.animate', name='animate'),

    url(r'greeting/$', 'openbar_users.views.greeting'),
    url(r'username/$', 'openbar_users.views.username'),

    url(r'^show_login/$', 'openbar_users.views.login_page', name='show_login'),
    url(r'^accounts/login/$', 'openbar_users.views.app_login', name='login'),
    url(r'^accounts/logout/$', 'openbar_users.views.app_logout', name='logout'),
    url(r'^create_account/$', 'openbar_users.views.create_account', name='create_account'),
    url(r'^searcher/new/$', 'openbar_users.views.create_searcher', name='new_searcher'),
    url(r'^home/$', 'openbar_users.views.home_view', name='homepage'),
    url(r'^preference/new$', 'openbar_search.views.add_preference', name='new_preference'),
    url(r'^search/$', 'openbar_search.views.search', name='search'),
    url(r'^results/$', 'openbar_search.views.results', name='results'),
    url(r'^increase_complexity_score', 'openbar_search.views.increase_complexity_score', name='increase_complexity_query'),
    url(r'^decrease_complexity_score', 'openbar_search.views.decrease_complexity_score', name='decrease_complexity_query'),
    url(r'^set_complexity_score', 'openbar_search.views.set_complexity_score', name='set_complexity_query'),


    url(r'^create_folder/$', 'openbar_users.views.create_folder', name='create_folder'),
    url(r'^add_subfolder/$', 'openbar_users.views.add_subfolder', name='create_subfolder'),
    url(r'^add_item/$', 'openbar_users.views.add_item', name='create_item'),
    url(r'^remove_item/$', 'openbar_users.views.remove_item', name='remove_item'),
    url(r'^remove_subfolder/$', 'openbar_users.views.remove_subfolder', name='remove_subfolder'),

    url(r'^get_user_complexity_score/$', 'openbar_users.views.get_user_complexity_score', name='get_user_cs'),

    url(r'^get_followed_links/$', 'openbar_users.views.get_users_followed_links'),
    url(r'^follow_link/$', 'openbar_users.views.follow_link', name='follow_link'),
    url(r'^reviewed_link/$', 'openbar_users.views.reviewed_link'),


    url(r'^voodoo/599aaf818f60edbb2c001784f19217dd/randomize_complexity',
        'openbar_search.complexilizer.randomize_complexity'),
    url(r'^voodoo/normalize', 'openbar_search.views.normalize_scores'),
    url(r'^voodoo/search_page', 'openbar_search.views.extension'),
    url(r'^voodoo/get_random_query', 'openbar_search.views.get_random_query'),

    url(r'^extension/folders', 'openbar_users.views.get_folders'),
]
