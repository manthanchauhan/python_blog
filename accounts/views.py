from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import login


def signup(request):
    if request.user.is_authenticated:
        return redirect('home_url')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_url')
        return render(request, 'signup.html', {'form': form})

    elif request.method == 'GET':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})


# Create your views here.
