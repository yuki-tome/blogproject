from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost, Author
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import BlogPostForm
from django.db.models import Count
from django.contrib.auth.models import User

""" def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blogapp/blog_list.html', {'posts': posts}) """

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-date')
    authors = Author.objects.annotate(num_posts=Count('blogpost'))
    return render(request, 'blogapp/blog_list.html', {'posts': posts, 'authors': authors})

def blog_detail(request, pk):
    post = BlogPost.objects.get(pk=pk)
    return render(request, 'blogapp/blog_detail.html', {'post': post})

""" def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("User logged in")
        else:
            return HttpResponse("Invalid credentials")
    else:
        form = AuthenticationForm()  # フォームのインスタンスを作成
        return render(request, 'blogapp/login.html', {'form': form})  # フォームをテンプレートに渡す """

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog_list')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()  # フォームのインスタンスを作成
    return render(request, 'blogapp/login.html', {'form': form})  # フォームをテンプレートに渡す

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return render(request, 'blogapp/logout_confirmation.html')
    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Author.objects.create(user=user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/register.html', {'form': form})

""" def blog_post_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = Author.objects.get(user=request.user)
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blogapp/blog_post_form.html', {'form': form}) """

def blog_post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)  # save the form but don't commit to the database yet
            new_post.author = Author.objects.get(user=request.user)  # assign the logged in user as the author
            new_post.save()  # now save the post to the database
            return redirect('blog_list')  # redirect to the blog list page
    else:
        form = BlogPostForm()
    return render(request, 'blogapp/blog_post_form.html', {'form': form})

def author_posts(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    posts = BlogPost.objects.filter(author=author)
    # 他の著者を取得します。
    other_authors = Author.objects.exclude(id=author_id)

    context = {
        'author': author,
        'posts': posts,
        'other_authors': other_authors,
    }
    
    return render(request, 'blogapp/author_posts.html', context)