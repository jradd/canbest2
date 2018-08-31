from django.conf.urls import url
from .views import (
    CommentCreateApiView,
    CommentListApiView,
    CommentDetailApiView,
    CommentEditAPIView,
)

urlpatterns = [
    url(r'^$', CommentListApiView.as_view(), name='list'),
    url(r'^create/$', CommentCreateApiView.as_view(), name='create'),
    url(r'^(?P<id>[-\w]+)/$', CommentDetailApiView.as_view(), name='detail'),
    url(r'^(?P<id>[-\w]+)/edit$', CommentEditAPIView.as_view(), name='edit'),
]
