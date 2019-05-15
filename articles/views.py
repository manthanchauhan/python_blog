from django.shortcuts import render, redirect
from .models import Article
from . import models
from . import forms
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from boards import models as board_models


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
        print(request.POST)
        if 'new' in request.POST.keys():
            print(request.FILES)
            form = forms.NewArticleForm(request.POST, request.FILES)
            if form.is_valid():
                # print(form.cleaned_data)
                article_ = form.save()
                board_models.Board.objects.create(article=article_)
                return redirect('home_url')

        elif 'del' in request.POST.keys():
            form = forms.DeleteArticle(request.POST)
            if form.is_valid():
                form = form.cleaned_data
                ids = form['title']

                for id_ in ids:
                    article_ = Article.objects.get(id=id_)
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(article_.content)))
                    os.remove(os.path.join(settings.MEDIA_ROOT, str(article_.thumbnail)))
                    article_.delete()
                return redirect('modify_articles_url')


@login_required(login_url='login_url')
def article_view(request, id_):
    article_ = Article.objects.get(id=id_)

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
                   })


@login_required(login_url='login_url')
def tag_view(request, id_):
    tag = models.Tag.objects.get(id=id_)
    return render(request, 'tag_view.html', {'tag': tag})


def mod_tags(request):
    if not request.user.is_superuser:
        return redirect('home_url')

    if request.method == 'GET':
        tags = models.Tag.objects.all()
        new_form = forms.NewTagForm()
        del_form = forms.DeleteTagForm()

        return render(request, 'mod_tag.html',
                      {'new_form': new_form,
                       'del_form': del_form,
                       'tags': tags,
                       })

    elif request.method == 'POST':
        if 'new' in request.POST.keys():
            form = forms.NewTagForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                author = request.user

                models.Tag.objects.create(title=title,
                                          description=description,
                                          author=author)
                return redirect('modify_tags_url')

            tags = models.Tag.objects.all()
            new_form = forms.NewTagForm()
            del_form = forms.DeleteTagForm()
            return render(request, 'mod_tag.html',
                          {'new_form': new_form,
                           'del_form': del_form,
                           'tags': tags,
                           })

        elif 'del' in request.POST.keys():
            form = forms.DeleteTagForm()
            if form.is_valid():
                form = form.cleaned_data
                ids = form['title']

                for id_ in ids:
                    models.Tag.objects.get(id=id_).delete()

                return redirect('home_url')

            tags = models.Tag.objects.all()
            new_form = forms.NewTagForm()
            del_form = forms.DeleteTagForm()
            return render(request, 'mod_tag.html',
                          {'new_form': new_form,
                           'del_form': del_form,
                           'tags': tags,
                           })
