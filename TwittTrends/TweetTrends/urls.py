from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index, name='index'),
    url(r'^post/$', views.Post, name='post'),
    url(r'^snsrequest/$', views.snsrequest),
    url(r'^polling/$', views.polling)
]