from django.db import models

from customauth.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリー')
    slug = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100, verbose_name='タイトル')
    body = models.TextField(verbose_name='本文')
    thumbnail = models.ImageField(null=True, blank=True, verbose_name='画像')
    posted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='コメント')
    posted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
