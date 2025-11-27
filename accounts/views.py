from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm, SignupForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signin')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect('main')  
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    form = SigninForm()
    return render(request, 'accounts/signin.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main')