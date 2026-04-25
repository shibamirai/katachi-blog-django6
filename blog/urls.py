from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('posts', views.MyPostListView.as_view(), name='mylist'),
    path('posts/create', views.PostCreateView.as_view(), name='create'),
    path('posts/<slug:slug>', views.PostView.as_view(), name='detail'),
    path('posts/<slug:slug>/update', views.PostUpdateView.as_view(), name='update'),
    path('posts/<slug:slug>/delete', views.PostDeleteView.as_view(), name='delete'),
]
