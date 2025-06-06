from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('forum/', views.forum_view, name='forum'),  # forum 页面
    path('logout/', views.logout_view, name='logout'),  # 添加登出路径
    path('get-posts/', views.get_posts, name='get_posts'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/comments/', views.get_comments, name='get_comments'),
    path('posts/<int:post_id>/comments/create/', views.create_comment, name='create_comment'),
]