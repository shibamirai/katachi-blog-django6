from django import forms

from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'thumbnail', 'body', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "input w-full"
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                "class": "file-input w-full"
            }),
            'body': forms.Textarea(attrs={
                "class": "textarea w-full"
            }),
            'category': forms.Select(attrs={
                "class": "select w-full"
            })
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                "class": "textarea w-full",
                "placeholder": "コメントを残す",
                "rows": "3"
            }),
        }
        labels = {
            'body': ''
        }