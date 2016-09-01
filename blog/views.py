from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, ContactForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.core.mail import EmailMessage
from django.template.loader import get_template

# Create your views here.


def post_list(request):
    # check if post is published, if not, it will not be displayed.
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    # check if post detail page exists by primary key
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        # form validation
        if form.is_valid():

            # commit false to prevent save form, because author isnt filled in by the user
            post = form.save(commit=False)
            post.author = request.user
            # function to post new blogpost instantly if uncommented.
            # post.published_date = timezone.now()
            post.save()

            # redirect user to post detail page using its primary key
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            # function to post new post instantly if uncommented.
            # post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    # filter posts by empty published date (unpublished posts)
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        data = dict(queryDict)

        form = data

        if form.is_valid:

            contact_name = data['contact_name']
            contact_email = data['contact_email']
            form_content = data['content']

            # put all form information in variables and stick it into a template
            template = get_template('contact/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            # create email which sends the mail with information from the form
            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" + '',
                ['v_dejong@icloud.com'],
                headers = {'Reply-To': contact_email}
            )

            email.send()
            return redirect('contact')

    else:
        form_class = ContactForm

    return render(request, 'contact/contactform.html', {'form': form_class})

