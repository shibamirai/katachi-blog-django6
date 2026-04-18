from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from .models import Category, Post


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

        category = self.request.GET.get('category')
        if category is not None:
            queryset = queryset.filter(
                category_id=category 
            )

        author = self.request.GET.get('author')
        if author is not None:
            queryset = queryset.filter(
                author_id=author 
            )
        
        return queryset.select_related('category').order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = Category.objects.filter(id=self.request.GET.get('category')).first()
        return context


class PostView(generic.DetailView):
    template_name = 'blog/posts/detail.html'
    queryset = Post.objects.select_related('category').select_related('author')
