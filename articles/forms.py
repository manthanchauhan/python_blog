from django import forms
from django.forms import ModelForm
from . import models


class NewArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = ['title',
                  'description',
                  'authors',
                  'tags',
                  'content',
                  'thumbnail',
                  ]


class DeleteArticle(forms.Form):
    choice = []

    for article in models.Article.objects.all():
        choice.append((article.id, article.title))

    title = forms.MultipleChoiceField(choices=choice)


class NewTagForm(ModelForm):
    class Meta:
        model = models.Tag
        fields = ['title',
                  'description',
                  ]


class DeleteTagForm(forms.Form):
    choice = []

    for tag in models.Tag.objects.all():
        choice.append((tag.id, tag.title))

    title = forms.MultipleChoiceField(choices=choice)

