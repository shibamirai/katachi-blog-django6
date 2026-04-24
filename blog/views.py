from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import PostForm
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


class PostDetailView(generic.DetailView):
    template_name = 'blog/posts/detail.html'
    queryset = Post.objects.select_related('category').select_related('author').prefetch_related('comment_set__author')


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'blog/posts/create.html'
    success_url = reverse_lazy('home')
    success_message = '「%(title)s」を投稿しました'

    def test_func(self):
        """管理者しかアクセスできないようにする"""
        return self.request.user.is_admin
    
    def form_valid(self, form):
        """モデルの保存前に、ログインユーザを投稿者とし
        スラッグには投稿日時分を'202510271318'形式の文字列にしてセットする
        """
        form.instance.author = self.request.user
        form.instance.slug = datetime.now().strftime('%Y%m%d%H%M')
        return super().form_valid(form)


class MyPostListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = 'blog/posts/mylist.html'
    model = Post
    paginate_by = 10

    def test_func(self):
        """管理者しかアクセスできないようにする"""
        return self.request.user.is_admin

    def get_queryset(self):
        """ログインユーザが投稿したものだけ表示"""
        queryset = super().get_queryset().filter(
            author_id=self.request.user.id
        )
        return queryset.select_related('category').order_by('-posted_at')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = PostForm
    template_name = 'blog/posts/edit.html'
    queryset = Post.objects.select_related('category').select_related('author')
    success_message = '「%(title)s」を更新しました'

    def test_func(self):
        """投稿者本人しかアクセスできないようにする"""
        post = self.get_object()
        return post.author == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'slug': self.object.slug})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """確認画面なしで記事を削除する
    確認画面を挟む場合は template_name で設定し GET でアクセスする
    """
    model = Post
    success_url = reverse_lazy('mylist')
    success_message = '「%(title)s」を削除しました'
    
    def test_func(self):
        """投稿者本人しかアクセスできないようにする"""
        post = self.get_object()
        return post.author == self.request.user

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title=self.object.title,
        )
