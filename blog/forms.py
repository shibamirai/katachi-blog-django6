from django import forms

from .models import Post

class PostCreateForm(forms.ModelForm):
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
