from django import forms
from . import models
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['content']
        labels = {'content': 'Query', }
        widgets = {'content': SummernoteWidget, }


class ReplyForm(PostForm):
    class Meta:
        model = models.Post
        fields = ['content']
        labels = {'content': 'Comment', }
        widgets = {'content': SummernoteWidget, }
