from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['content']
        labels = {'content': 'Query',
                  }


class ReplyForm(PostForm):
    class Meta:
        model = models.Post
        fields = ['content']
        labels = {'content': 'Comment',
                  }
