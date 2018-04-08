from django.conf.urls import url

from youtubeapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^videos/$', views.videos, name='videos'),
]