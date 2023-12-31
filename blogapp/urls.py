from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('create/', views.blog_post_create, name='blog_post_create'),
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    path('posts/<int:year>/<int:month>/<int:day>/', views.posts_on_date, name='posts_on_date'),
    path('calendar/', views.calendar_view, name='calendar_current'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('search/', views.blog_search, name='blog_search'),
]