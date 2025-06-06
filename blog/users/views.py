from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Post, Comment
import json
@csrf_exempt
def get_posts(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by('-date')  # 按日期降序排列
        data = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "date": post.date.strftime('%Y-%m-%d'),
                "category": post.category,
            }
            for post in posts
        ]
        return JsonResponse(data, safe=False)

@csrf_exempt
def create_post(request):
    if request.method == "POST":
        body = json.loads(request.body)
        new_post = Post.objects.create(
            title=body["title"],
            content=body["content"],
            author=body["author"],
            category=body["category"]
        )
        return JsonResponse({"message": "Post created successfully", "post_id": new_post.id})

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # 清除用户登录状态
        return JsonResponse({'message': '登出成功'}, status=200)
    return JsonResponse({'message': '无效的请求方法'}, status=405)
@login_required
def forum_view(request):
    # 渲染 forum.html 模板
    return render(request, 'forum.html')
@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            # 解析 JSON 数据
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'message': '请求数据格式错误'}, status=400)

            # 获取数据
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')

            # 验证数据完整性
            if not username or not password or not confirm_password:
                return JsonResponse({'message': '用户名或密码不能为空'}, status=400)

            # 验证两次密码是否一致
            if password != confirm_password:
                return JsonResponse({'message': '两次输入的密码不一致'}, status=400)

            # 检查用户名是否已被注册
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': '用户名已被注册'}, status=400)

            # 创建新用户（自动加密密码）
            User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': '注册成功'}, status=201)

        except Exception as e:
            return JsonResponse({'message': f'服务器错误: {str(e)}'}, status=500)
    return JsonResponse({'message': '无效的请求方法'}, status=405)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # 使用 authenticate 验证用户
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # 登录成功后跳转到 forum 页面
                return JsonResponse({'message': '登录成功', 'redirect_url': '/forum/'}, status=200)
            else:
                return JsonResponse({'message': '用户名或密码错误'}, status=401)

        except Exception as e:
            return JsonResponse({'message': f'服务器错误: {str(e)}'}, status=500)
    return JsonResponse({'message': '无效的请求方法'}, status=405)

@csrf_exempt
def get_comments(request, post_id):
    if request.method == "GET":
        comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
        data = [{
            "id": comment.id,
            "content": comment.content,
            "author": comment.author,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        return JsonResponse(data, safe=False)

@csrf_exempt
def create_comment(request, post_id):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            new_comment = Comment.objects.create(
                post_id=post_id,
                content=body["content"],
                author=body["author"]
            )
            return JsonResponse({
                "message": "评论发布成功",
                "comment_id": new_comment.id
            })
        except Exception as e:
            return JsonResponse({"message": f"评论发布失败: {str(e)}"}, status=400)
