from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework_simplejwt.tokens import RefreshToken


def login_page(request):
    if request.method == "POST":
        user = authenticate(
            request=request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if not user:
            return render(
                request, "messaging/login.html", {"error": "Credenciais inválidas"}
            )

        login(request, user)

        refresh = RefreshToken.for_user(user)
        request.session["access"] = str(refresh.access_token)
        request.session["refresh"] = str(refresh)

        return redirect("chat")

    return render(request, "messaging/login.html")


def register_page(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(
                request, "messaging/register.html", {"error": "Usuário já existe"}
            )

        User.objects.create_user(
            username=request.POST.get("username"), password=request.POST.get("password")
        )

        return redirect("login-page")

    return render(request, "messaging/register.html")


@login_required(login_url="/login-page/")
def chat_page(request):
    access_token = request.session.get("access")

    if not access_token:
        return redirect("login-page")

    return render(request, "messaging/chat.html", {"token": access_token})


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("login-page")
