from django.shortcuts import render, redirect
from . import models
from . import forms


def board_view(request, id_):
    if request.method == 'GET':
        brd = models.Board.objects.get(id=id_)
        form = forms.PostForm()
        context = {}
        return render(request, 'board.html', {'board': brd,
                                              'form': form}, context)

    elif request.method == 'POST':
        print(request.POST)
        if 'query' in request.POST.keys():
            form = forms.PostForm(request.POST)
            print(request.POST)
            print(form.errors)
            if form.is_valid():
                form = form.cleaned_data
                content = form['content']
                brd = models.Board.objects.get(id=id_)
                models.Post.objects.create(content=content,
                                           author=request.user,
                                           board=brd,
                                           )
            return redirect(request.path)

        else:
            print(request.POST)
            print("hi")
            return redirect('home_url')
