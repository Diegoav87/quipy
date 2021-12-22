from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user
from .forms import CustomUserForm

# Create your views here.


@unauthenticated_user
def register(request):
    form = CustomUserForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:login-user')

    return render(request, 'accounts/register.html', {"form": form})


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, "Email or password are incorrect")

    return render(request, 'accounts/login_user.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts:login-user')
