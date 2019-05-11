from django.shortcuts import render, redirect
from .models import Article
from . import forms
import os
# from django.http import HttpResponse


def home_view(request):
    all_articles = Article.objects.all()
    return render(request, 'home.html', {'articles': all_articles})


def mod_articles(request):
    if not request.user.is_superuser:
        return redirect('home_url')

    if request.method == 'GET':
        all_articles = Article.objects.all()
        new_article_form = forms.NewArticleForm()
        del_form = forms.DeleteArticle()
        return render(request, 'mod_article.html',
                      {'new_form': new_article_form,
                       'del_form': del_form,
                       'articles': all_articles,
                       })

    elif request.method == 'POST':
        if 'new' in request.POST.keys():
            form = forms.NewArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home_url')

        elif 'del' in request.POST.keys():
            form = forms.DeleteArticle(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                ids = form['title']

                for id_ in ids:
                    Article.objects.get(id=id_).delete()
                return redirect('modify_articles_url')


def article_view(request, id_):
    article_ = Article.objects.get(id=id_)

    from django.conf import settings
    from string import Template

    with open(os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'article_view.html'), 'r') as file:
        template = file.read()
        template = Template(template)

    with open(os.path.join(settings.MEDIA_ROOT, str(article_.content)), 'r') as content:
        html = template.substitute(content=content.read())

    with open(os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'temp_article.html'), 'w') as file:
        file.write(html)

    return render(request, 'temp_article.html',
                  {'article': article_,
                   'user': request.user
                   })
