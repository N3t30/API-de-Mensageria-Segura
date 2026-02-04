import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AuditLog, Message
from .serializers import MessageSerializer, RegisterSerializer

logger = logging.getLogger("django.security")



class LoginView(APIView):
    
    @ratelimit(key="ip", rate="5/m", block=True)
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )
        if not user:
            logger.warning(
                f"Falha de login | IP: {request.META.get('REMOTE_ADDR')} | user: {request.data.get('username')}"  # noqa E501
            )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({"detail": "logout realizado com sucesso"})


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            messages = Message.objects.all()
        else:
            messages = Message.objects.filter(
                Q(sender=request.user) | Q(recipient=request.user)
            )

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response(status=404)

        is_participant = (
            message.sender == request.user or
            message.recipient == request.user
        )

        if not is_participant and not request.user.is_staff:
            AuditLog.objects.create(
                user=request.user,
                action="UNAUTHORIZED_ACCESS",
                target=f"message:{message.id}",
            )
            return Response(status=403)

        serializer = MessageSerializer(message)
        return Response(serializer.data)


class MessageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
