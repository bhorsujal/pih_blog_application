from django.shortcuts import render, redirect
# from django.http import HttpResponse
from .models import Post     #. implies from the same directory import post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import (LoginRequiredMixin,      #check for required conditions before executing a function
                                        UserPassesTestMixin      #used for confirming user before post edit
                                        )    

from django.views.generic import(   ListView,           #used for post display on home-page
                                    DetailView,         #used to display posts in detail
                                    CreateView,         #create posts
                                    UpdateView,         #update posts
                                    DeleteView          #delete posts
                                )         


# Create your views here.
# def home(request):
#     context = {
#         'posts': Post.objects.all()     #  <-----The query is here
#     }
#     return render(request, 'blog/home.html', context)

#class based views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']   #orders the posts from oldest to newest, but if '-' then newest to oldest

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):             #returns the author to the post on new post
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', { 'title' : 'About'})


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('blog/home.html')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('blog/home.html')

        if len(username) > 10:
            messages.error(request, "Username exceeds 10 characters!")
            return redirect('blog/home.html')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('blog/home.html')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('blog/home.html')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        
        return redirect('signin')
        
        
    return render(request, "blog/signup.html")


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']

        my_user = authenticate(username=username, password=pass1)

        if my_user is not None:
            login(request, my_user)
            first_name = my_user.first_name
            return render(request, "blog/home.html", {"first_name": first_name})
        else:
            messages.error(request, "Wrong Credentials.")
            return redirect('blog-home')

    return render(request, "blog/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('blog-home')
