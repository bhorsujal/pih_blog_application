from django.shortcuts import render, redirect , get_object_or_404
# from django.http import HttpResponse
from .models import Category, Post, Comment    
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
from .forms import  CommentForm, PostForm
from django.views import View
from django.http import HttpResponseBadRequest
from django.db.models import Count
from .forms import SearchForm

# Create your views here.
# def home(request):
#     context = {
#         'posts': Post.objects.all()     #  <-----The query is here
#     }
#     return render(request, 'blog/home.html', context)

#class based views

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all categories and annotate the count of posts in each category
        categories = Category.objects.annotate(post_count=Count('post'))

        if not self.object_list:
            context['posts'] = []

        sort_by = self.request.GET.get('sort_by', 'newest')
        if sort_by not in ['title', 'likes', 'newest', 'oldest']:
            sort_by = 'newest'

        if self.request.user.is_authenticated:
            user = self.request.user
            context['liked_posts'] = self.request.user.liked_posts.all()

        most_liked_post = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count').first()

        context['most_liked_post'] = most_liked_post
        context['categories'] = categories  # Pass categories to the context
        context['active_category'] = self.kwargs.get('category_id', None)  # Add this line

        return context

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by','newest')
        if sort_by == 'title':
            return Post.objects.order_by('title')
        elif sort_by == 'likes' :
            return Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        elif sort_by == 'newest':
            return Post.objects.order_by('-date_posted')
        elif sort_by == 'oldest':
            return Post.objects.order_by('date_posted')


class PostsByCategoryView(PostListView):
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        sort_by = self.request.GET.get('sort_by', 'newest')
        queryset = Post.objects.filter(category__id=category_id)

        if sort_by == 'title':
            queryset = queryset.order_by('title')
        elif sort_by == 'likes':
            queryset = queryset.annotate(like_count=Count('likes')).order_by('-like_count', '-date_posted')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-date_posted')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('date_posted')

        return queryset


class LikeView(LoginRequiredMixin,View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user.id)
        else:
            post.likes.add(request.user.id)

        return redirect('post-detail', pk=pk)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        # Check if the user is logged in before allowing comments
        if self.request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = self.request.user  # Assign the logged-in user to the comment
                comment.save()
                return redirect('post-detail', pk=post.pk)
        else:
            # Handle the case where the user is not logged in
            return redirect('login')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'image']
    # template_name = 'blog/post_form.html'  # You should have a custom template for creating a post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SearchView(View):
    template_name = 'blog/search_results.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query', '')
            print("Search Query:", query)  # Add this line

            results = Post.objects.filter(title__icontains=query, content__icontains=query)
            print("Search Results:", results)  # Add this line
        else:
            results = []
        context = {
            'form': form,
            'results': results,
        }

        return render(request, self.template_name, context)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'image']

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


def search_view(request):
    form = SearchForm(request.GET)
    query = form['query'].value()

    # results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    results = Post.objects.filter(title__icontains=query)

    context = {
        'search_form': form,
        'results': results,
    }

    return render(request, 'blog/search_results.html', context)