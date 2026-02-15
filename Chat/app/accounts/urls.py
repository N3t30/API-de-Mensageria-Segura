from django.urls import path

from .views import (LoginView, RegisterView, MessageCreateView, MessageDetailView, check_username, MessageCreateView)

urlpatterns = [
    path('messages/', MessageCreateView.as_view(), name='create-message'),
    path('messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
    path('messages/create/', MessageCreateView.as_view(), name='create-message'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("check-username/", check_username, name="check-username"),
]
