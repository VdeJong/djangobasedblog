from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm




# Create your views here.

def post_list(request):
    # check if post is published, if not, it will not be displayed.
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post' : post})

def new_post(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})