from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('posts/<slug:slug>', views.PostView.as_view(), name='detail'),
]
