from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import UserProfile


def login_user(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)

        if not email:
            messages.error(request, "E-mail é necessário")
            return redirect("login")
        
        if not password:
            messages.error(request, "Senha vazia")
            return redirect("login")

        user = authenticate(
            request=request,
            email=email,
            password=password
        )

        if not user:
            messages.error(request, "Erro ao realizar o login")
            return redirect("login")
        
        login(request, user)
        return redirect("home")

    else:
        return render(request, "login.html", {})

def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, "Sessão encerrada com sucesso!")
    return redirect("login")

def register_user(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        password_validation = request.POST.get("password_validation", None)

        if not (password == password_validation):
            messages.error(request, "As senhas não são iguais!")
            return redirect("register")
        
        user = UserProfile.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        if not user:
            messages.error(request, "Erro ao criar seu usuário, tente novamente.")
            return redirect("register")
        
        return redirect("login")
    
    else:
        return render(request, 'register.html', {})