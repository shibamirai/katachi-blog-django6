from django.db import models

from customauth.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    slug = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
