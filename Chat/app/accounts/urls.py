from django.urls import path

from .views import MessageCreateView, MessageDetailView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('messages/', MessageCreateView.as_view(), name='create-message'),
    path('messages/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
]
