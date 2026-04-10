from django.contrib import admin

from blog.models import Category
from blog.models import Post

admin.site.register(Category)
admin.site.register(Post)
