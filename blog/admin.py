from django.contrib import admin

from blog.models import Category, Comment, Post

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
