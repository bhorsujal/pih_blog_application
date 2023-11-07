from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # path('', views.home, name = 'blog-home'),     
    path('', PostListView.as_view(), name = 'blog-home'),   #searches for <app>/<model>_<viewtype>.html
    path('about/', views.about, name = 'blog-about'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),  #pk is the primary key of post   
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),     #searches for <app>/<form>.html
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
]
