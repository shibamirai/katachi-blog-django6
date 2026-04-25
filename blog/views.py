from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


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


class PostView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = CommentCreateFormView.as_view()
        return view(request, *args, **kwargs)


class PostDetailView(generic.DetailView):
    """PostView への GET リクエストで呼ばれる
    DetailView にコメント作成フォームを追加している
    """
    template_name = 'blog/posts/detail.html'
    queryset = Post.objects.select_related('category').select_related('author').prefetch_related('comment_set__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CommentCreateFormView(generic.detail.SingleObjectMixin, generic.FormView):
    """PostView への POST リクエストで呼ばれる
    フォームの処理を行うため FormView を継承する
    URL から特定した Post に対してコメントを付与するため、SingleObjectMixin で model に Post を指定する
    """
    template_name = 'blog/posts/detail.html'    # バリデーションエラー時に編集画面に戻すために必要
    form_class = CommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.post = self.get_object()   # URL から特定した Post をインスタンスフィールドとして保存
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail', kwargs={'slug': self.post.slug})

    def form_valid(self, form):
        # 「ログインユーザが投稿したこの Post へのコメント」として保存
        form.instance.post = self.post
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


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


class CommentDetailView(generic.DetailView):
    template_name = 'cotton/blog/comment/index.html'
    model = Comment


class CommentUpdateView(UserPassesTestMixin, generic.UpdateView):
    template_name = 'cotton/blog/comment/update.html'
    model = Comment
    form_class = CommentForm

    def test_func(self):
        # 投稿者本人しかアクセスできないようにする
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse('comment', kwargs={'pk': self.get_object().id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment

    def get_object(self):
        """コメント削除後に元の記事詳細画面に戻るために記事のスラッグを保存しておく"""
        object = super().get_object()
        self.slug = Post.objects.get(pk=object.post_id).slug
        return object

    def test_func(self):
        # 投稿者本人しかアクセスできないようにする
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse('detail', kwargs={'slug': self.slug})
