from django import forms
from .models import Post

class PostForm(forms.Modelform):
    class meta:
        model = Post
        fields = ('title',
                  'text',)
