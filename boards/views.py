from django.shortcuts import render, redirect, reverse
from . import models
from . import forms
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache


@csrf_protect
def board_view(request, id_):
    if request.method == 'GET':
        brd = models.Board.objects.get(id=id_)
        form = forms.PostForm()
        context = {}
        return render(request, 'board.html', {'board': brd,
                                              'form': form}, context)

    elif request.method == 'POST':
        # print(request.POST)
        if 'query' in request.POST.keys():
            # print(request.POST)
            form = forms.PostForm(request.POST)
            print(request.POST)
            # print(form.errors)
            if form.is_valid():
                form = form.cleaned_data
                content = form['content']
                brd = models.Board.objects.get(id=id_)
                post = models.Post.objects.create(content=content,
                                                  author=request.user,
                                                  board=brd,
                                                  )
                brd.last_update = post.created_on
                brd.save(update_fields=['last_update'])

            return redirect(request.path)

        else:
            if 'reply' in request.POST.keys():
                id_ = int(request.POST['reply'])
                url = reverse('reply_url', kwargs={'id_': id_})
                return redirect(url)
            return redirect('home_url')


@never_cache
def reply_view(request, id_):
    if request.method == 'GET':
        post = models.Post.objects.get(id=id_)
        form = forms.ReplyForm()
        return render(request, 'reply_view.html', {'form': form,
                                                   'post': post,
                                                   })
    elif request.method == 'POST':
        form = forms.ReplyForm(request.POST)
        if form.is_valid():
            rel_post = models.Post.objects.get(id=id_)
            brd = rel_post.board
            form = form.cleaned_data
            content = form['content']
            post = models.Post.objects.create(content=content,
                                              author=request.user,
                                              board=brd,
                                              parent_post=rel_post,
                                              )
            brd.last_update = post.created_on
            brd.save(update_fields=['last_update'])
            url = reverse('board_url', kwargs={'id_': brd.id})
            return redirect(url)

        return redirect('home_url')
