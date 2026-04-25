from django.urls import path
from django.views.decorators.http import require_POST

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('posts', views.MyPostListView.as_view(), name='mylist'),
    path('posts/create', views.PostCreateView.as_view(), name='create'),
    path('posts/<slug:slug>', views.PostView.as_view(), name='detail'),
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(), name='update'),
    path('posts/<slug:slug>/delete', require_POST(views.PostDeleteView.as_view()), name='delete'),
    path('comment/<pk>', views.CommentDetailView.as_view(), name='comment'),
    path('comment/<pk>/update', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<pk>/delete', require_POST(views.CommentDeleteView.as_view()), name='comment-delete')
]
