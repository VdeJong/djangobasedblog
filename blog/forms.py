from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author',
                  'text')

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label='Your Email:')
    contact_email = forms.EmailField(required=True, label='Your Name:')
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label='What do you want to say?'
    )
