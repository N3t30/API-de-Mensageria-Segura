from django.urls import path

from .views import chat_page, login_page, logout_view, register_page

urlpatterns = [
    path("login/", login_page, name="login-page"),
    path("register/", register_page, name="register-page"),
    path("password-reset/", login_page, name="password_reset"),
    path("chat/", chat_page, name="chat"),
    path("logout/", logout_view, name="logout"),
]
