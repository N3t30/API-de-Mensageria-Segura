from django.shortcuts import render

def login_page(request):
    return render(request, "messaging/login.html")

def register_page(request):
    return render(request, "messaging/register.html")

