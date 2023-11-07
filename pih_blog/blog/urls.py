from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostsByCategoryView, UserPostListView
urlpatterns = [
    # path('', views.home, name = 'blog-home'),     
    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),   #searches for <app>/<model>_<viewtype>.html
    path('about/', views.about, name = 'blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),  #pk is the primary key of post   
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),     #searches for <app>/<form>.html
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    # path('blog/', PostListView.as_view(), name = 'blog-name'),
    path('search/', views.search, name='search'),
    path('like/<int:pk>/', views.LikeView.as_view(), name='like'),
    path('category/<int:category_id>/', PostsByCategoryView.as_view(), name='category-posts'),
]
