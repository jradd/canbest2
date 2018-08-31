from django.conf.urls import url
from .views import (
    PostCreateApiView,
    PostDeleteApiView,
    PostDetailApiView,
    PostListApiView,
    PostUpdateApiView,
)

urlpatterns = [
    url(r'^$', PostListApiView.as_view(), name='list'),
    url(r'^create/$', PostCreateApiView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailApiView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateApiView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteApiView.as_view(), name='delete'),
]
