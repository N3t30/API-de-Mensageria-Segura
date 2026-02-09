from django.urls import path

from .views import (LoginView, RegisterView, MessageCreateView, MessageDetailView, UserListView)

urlpatterns = [
    path('messages/', MessageCreateView.as_view(), name='create-message'),
    path('messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user-list"),
]
