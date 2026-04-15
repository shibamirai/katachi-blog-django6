from django.shortcuts import render
from django.views import generic

from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/posts/list.html'
    model = Post
    queryset = Post.objects.select_related('category').order_by('-posted_at')
