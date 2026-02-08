from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import login

def login_page(request):
    if request.method == "POST":
        user = authenticate(
            request=request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if not user:
            return render(
                request,
                "messaging/login.html",
                {"error": "Credenciais inválidas"}
            )
        
        login(request, user)

        refresh = RefreshToken.for_user(user)
        request.session["access"] = str(refresh.access_token)
        request.session["refresh"] = str(refresh)

        return redirect("chat-page")

    return render(request, "messaging/login.html")


def register_page(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(
                request,
                "messaging/register.html",
                {"error": "Usuário já existe"}
            )

        User.objects.create_user(
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        return redirect("login-page")

    return render(request, "messaging/register.html")

def chat_page(request):
    accsse_token = request.session.get("access")

    if not accsse_token:
        return redirect("login-page")
    
    return render(request, "messaging/chat.html", {
        "token": request.session.get("access")
    })