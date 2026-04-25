from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует!')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Добро пожаловать!')
        return redirect('home')

    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Вы вошли в систему!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    
    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы!')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Аккаунт удалён!')
        return redirect('home')
    
    return render(request, 'users/delete_account.html')
