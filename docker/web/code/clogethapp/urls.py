from django.conf.urls import  url
from . import views
# from .models import Post
# from django.views.generic import ListView, DetailView


urlpatterns = [
    url(r'^$', views.post_home, name='post_home'),
    url(r'block/(?P<pk>\d+)/$', views.block, name='block'),
    url(r'tx/(?P<pk>\d+)/$', views.tx, name='tx'),
    url(r'addr/(?P<pk>\d+)/$', views.addr, name='addr'),
    url(r'stat//$', views.addr, name='stat'),

]

