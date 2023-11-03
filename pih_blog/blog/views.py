from django.shortcuts import render, redirect , get_object_or_404
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
    paginate_by = 3

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


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

