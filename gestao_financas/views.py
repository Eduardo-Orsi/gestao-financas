from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required

from .models import Wallet


@login_required()
def home(request: HttpRequest):
    return render(request, 'home.html', {})

@login_required()
def profile(request: HttpRequest):
    return render(request, "profile.html", {})

@login_required()
def wallet(request: HttpRequest, pk = None):
    user_id = request.user.id
    if pk:
        wallet = Wallet.objects.get(id=pk)
        context = {
            "wallet": wallet
        }
        return render(request, 'add_wallet.html', context)

    user_wallets = Wallet.objects.filter(user_id=user_id)
    context = {
        "wallets": user_wallets
    }

    return render(request, 'wallet.html', context)

@login_required()
def add_wallet(request: HttpRequest):

    if request.method == "POST":
        name = request.POST.get("name", None)
        description = request.POST.get("description", None)

        if not name:
            messages.error(request, "Nome da certeira é necessário")
            return render(request, "add_wallet.html", {})
        
        wallet = Wallet(
            user_id = request.user,
            name = name,
            description = description
        )

        if not wallet:
            messages.error(request, "Erro ao salvar sua carteira")

        wallet.save()
        return redirect("wallet")
        
    else:
        return render(request, 'add_wallet.html', {})

@login_required()
def transactions(request: HttpRequest):
    return render(request, 'transactions.html', {})

@login_required()
def add_transaction(request: HttpRequest):
    if request.method == "POST":
        return render(request, 'add_transaction.html', {})
    else:
        return render(request, 'add_transaction.html', {})

@login_required()
def categorys(request: HttpRequest):
    return render(request, 'categorys.html', {})

@login_required()
def add_categorys(request: HttpRequest):

    if request.method == "POST":
        return render(request, 'add_category.html', {})
    else:
        return render(request, 'add_category.html', {})

@login_required()
def reports(request: HttpRequest):
    return render(request, 'reports.html', {})

@login_required()
def add_report(request: HttpRequest):
    if request.method == "POST":
        return render(request, 'add_report.html', {})
    else:
        return render(request, 'add_report.html', {})