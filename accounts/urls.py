from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views
from .forms import PasswordResetForm, PasswordResetConfirmForm


app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>)/",
         views.account_activate, name="activate"),
    path('login-user/', views.login_user, name="login-user"),
    path('logout/', views.logout_user, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('edit-account/', views.edit_account, name="edit_account"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
        success_url="password_reset_email_confirm/",
        email_template_name="accounts/password_reset_email.html",
        form_class=PasswordResetForm
    ), name="password_reset"),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/accounts/password_reset_complete/",
            form_class=PasswordResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="accounts/reset_status.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(template_name="accounts/reset_status.html"),
        name="password_reset_complete",
    ),
]
