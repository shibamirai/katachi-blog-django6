from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/posts/list.html'
    model = Post
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search')
        if search is not None:
            queryset = queryset.filter(
                Q(title__contains=search) | Q(body__contains=search)
            )
        
        return queryset.select_related('category').order_by('-posted_at')