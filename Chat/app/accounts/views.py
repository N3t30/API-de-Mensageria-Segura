from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
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


# Responsável por autenticar o usuário, aplicar rate limit e registrar tentativas de login inválidas
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
            return Response(
                {"error": "Credenciais inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
       
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)

# Responsável por registrar novos usuários no sistema
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Responsável por invalidar o refresh token e encerrar a sessão do usuário autenticado
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({"detail": "logout realizado com sucesso"})

# Responsável por listar mensagens do usuário ou todas as mensagens se for administrador
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        base_filter  = Message.objects.filter(
                is_expired=False
                ).filter(
                    Q(expires_at_isnull=True) | Q(expires_at__gt=timezone())
                )
        
        if request.user.is_staff:
            messages = base_filter
        else:
            messages = base_filter.filter(
                Q(sender=request.user) | Q(recipient=request.user)
            )

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

# Responsável por retornar uma mensagem específica, validando permissão e registrando acessos não autorizados
class MessageDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):
        try:
            message = Message.objects.get(
                id=message_id,
                is_expired=False
            )
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

# Responsável por criar uma nova mensagem associando automaticamente o remetente ao usuário autenticado
class MessageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# Responsável por criar uma nova mensagem, associando o remetente ao usuário autenticado e validando os dados de entrada
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
            username = request.data.get("username")
            content = request.data.get("content")
            ttl_seconds = request.data.get("ttl_seconds")
        
            if not username or not content:
                return Response(
                    {"error": "username e content são obrigatórios"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try: 
                recipient = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {"error": "Usuário destinatário não encontrado"},
                    status=status.HTTP_404_NOT_FOUND
            )
            
            Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content,
            ttl_seconds=ttl_seconds
            )      

            AuditLog.objects.create(
            user=request.user,
            action="SEND_MESSAGE",
            target=f"user:{recipient.username}"

            )

            return Response(
            {"detail": "Mensagem enviada com sucesso"},
            status=status.HTTP_201_CREATED
            )

def check_username(request):
    username = request.GET.get("username")

    exists = User.objects.filter(username=username).exists()

    return JsonResponse({"exists": exists})

