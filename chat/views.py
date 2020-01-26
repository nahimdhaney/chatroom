# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import auth


def index(request):
    if request.user.is_authenticated:
        return render(request, 'chat/index.html', {
            'username': request.user.username
        })
    else:
        return redirect('login')


@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': request.user.username
    })


"""Users views."""


def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username and password'})
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'users/login.html')


def logout_view(request):
    """Logout view."""
    auth.logout(request)
    return render(request, 'users/login.html')
