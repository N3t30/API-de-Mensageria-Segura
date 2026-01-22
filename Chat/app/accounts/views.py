from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Message
from .serializers import MessageSerializer, RegisterSerializer


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


"""View para registro de novos usuários, só aceita POST, válida dados, não vaza senha
usa hash e bloqueia usuarios já autenticaddos de se registrar"""


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        )

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
