from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SigInUpform
from django.contrib.auth.models import User

def home(request):
    return render(
        request,
        'home.html'
    )


def signup_view(request):
    if request.method == 'POST':
        form = SigInUpform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('/')
            else:
                form.add_error('username', 'Имя занято')
    else:
        form = SigInUpform()
    return render(
        request,
        'signup.html',
        context={
            'form': form
        }
    )

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(
                    request,
                    'login.html',
                    context={
                        'form': form,
                        'invalid_login': True
                    }
                )
    else:
        form = LoginForm()
    
    return render(
        request,
        'login.html',
        context={
            'form': form
        }
    )

def logout_view(request):
    logout(request)
    return render(
        request,
        'logout.html'
    )
