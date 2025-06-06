from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('study', '学习'),
        ('help', '求助'),
        ('rant', '吐槽'),
        ('friend', '交友'),
    ]

    title = models.CharField(max_length=100)  # 帖子标题
    content = models.TextField()  # 帖子内容
    author = models.CharField(max_length=50)  # 作者
    date = models.DateField(auto_now_add=True)  # 发布日期
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)  # 分区

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()  # 评论内容
    author = models.CharField(max_length=50)  # 评论作者
    created_at = models.DateTimeField(auto_now_add=True)  # 评论时间
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
