from django.conf.urls import url
from django.contrib import admin
from .views import (
    battle_list,
    battle_create,
    battle_detail,
    battle_update,
    battle_delete,
    battle_result,
    battle_status_update,
    start_crawling,
    stop_crawling,
)

urlpatterns = [
    url(r'^$', battle_list, name='list'),
	url(r'^create/$', battle_create, name='create'),
    url(r'^(?P<id>\d+)/$', battle_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', battle_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', battle_delete, name='delete'),
    url(r'^(?P<id>\d+)/result/$', battle_result, name='result'),
    url(r'^update_status/(?P<id>\d+)/(?P<status>[R|D]{1})/$',
        battle_status_update, name='update_status'),
    url(r'^start_crawling/$', start_crawling, name='start_crawling'),
    url(r'^stop_crawling/$', stop_crawling, name='stop_crawling'),
]
