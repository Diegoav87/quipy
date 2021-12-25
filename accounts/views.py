from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string

from .decorators import unauthenticated_user
from .forms import CustomUserForm, UserEditForm
from .token import account_activation_token
from accounts.models import CustomUser

# Create your views here.


@unauthenticated_user
def register(request):
    form = CustomUserForm()

    if request.method == "POST":
        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "accounts/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            messages.success(
                request, "User registered successfully, an activation email has been sent")
            return redirect('accounts:login-user')

    return render(request, 'accounts/register.html', {"form": form})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Account activated successfully")
        return redirect("products:all_products")
    else:
        messages.error(request, "Account activation invalid")
        return redirect("products:all_products")


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('products:all_products')
        else:
            messages.error(request, "Email or password are incorrect")

    return render(request, 'accounts/login_user.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts:login-user')


@login_required
def dashboard(request):
    form = UserEditForm(instance=request.user)
    return render(request, "accounts/dashboard.html", {"form": form})


@login_required
def edit_account(request):
    if request.method == "POST":
        form = UserEditForm(instance=request.user,
                            data=request.POST, request=request)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been updated")
        return render(request, "accounts/dashboard.html", {"form": form})


@login_required
def delete_account(request):
    user = CustomUser.objects.get(username=request.user.username)
    user.is_active = False
    user.save()
    logout(request)
    messages.success(request, "User deleted successfully")
    return redirect("accounts:login-user")
