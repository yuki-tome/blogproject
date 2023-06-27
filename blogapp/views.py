from django.shortcuts import render, redirect
from .models import BlogPost
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blogapp/blog_list.html', {'posts': posts})

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
        return HttpResponse("Login form") """

def login_view(request):
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
        return render(request, 'blogapp/login.html', {'form': form})  # フォームをテンプレートに渡す

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return render(request, 'blogapp/logout_confirmation.html')