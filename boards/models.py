from django.db import models
from articles.models import Article
from django.contrib.auth.models import User


class Board(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='discussion_board')
    last_update = models.DateTimeField(null=True)


class Post(models.Model):
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='posts')
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children',
                                    default=None, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
# Create your models here.
