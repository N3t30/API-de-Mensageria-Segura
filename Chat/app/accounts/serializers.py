# Criando um serializer que trabalha diretamente com o modelor User padrão do django

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Message


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username já existe")
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username", read_only=True)
    recipient = serializers.CharField(source="recipient.username", read_only=True)

    # Aaqui somente para escrita, recebe ID
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "recipient",
            "content",
            "created_at",
        ]
        read_only_fields = ['sender', 'created_at']


# Serializer básico, recebe dados de registro, valida tamananho da senha
# impede vazamento da senha, controla campos aceitos, cria usuarios com senha criptografada
# INtegra com isistema de auth do Django
