from django.shortcuts import render, redirect, get_object_or_404
from post.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from post.models import BlogPost


def create(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('authenticate-url')
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # Create a BlogPost object but do not save it to the database yet (commit=False)
        obj = form.save(commit=False)
        # Get the author from the Account model based on the user's email
        author = Account.objects.filter(email=user.email).first()
        obj.author = author  # Set the author for the BlogPost object
        obj.save()  # save the BlogPost object to the db
        # Create a new instance of the CreateBlogPostForm to pass an empty form to the context
        form = CreateBlogPostForm()

    context['form'] = form

    return render(request, 'post/create.html', context)


def detail_blog(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'post/detail_blog.html', context)


def edit_blog(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('authenticate-url')

    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj
    form = UpdateBlogPostForm(
        initial={
            'title': blog_post.title,
            'body': blog_post.body,
            'price': blog_post.price,
            'image': blog_post.image,
        }
    )
    context['form'] = form
    return render(request, 'post/edit_blog.html', context)


def delete_blog(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate-url')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    # Check if the logged-in user is the author of the blog post
    if user == blog_post.author:
        # Delete the associated image file
        blog_post.image.delete(False)
        # Delete the blog post
        blog_post.delete()
        context['success_message'] = "DELETED"
        return render(request, 'post/deleted.html', context)  # Redirect to a success page or another page
