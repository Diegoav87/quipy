from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login-user/', views.login_user, name="login-user"),
    path('logout/', views.logout_user, name="logout"),
]
