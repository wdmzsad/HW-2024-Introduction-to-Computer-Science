from django.shortcuts import render
from django.urls import path, include
from users import views as user_views
urlpatterns = [
    path('users/', include('users.urls')),  # 确保包含 users 应用的路由
    path('', lambda request: render(request, 'login.html')),
    path('forum/', user_views.forum_view, name='forum'),  # forum 路径
]

