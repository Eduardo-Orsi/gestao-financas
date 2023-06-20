from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required

from .models import Wallet, RevenueCategory, ExpenseCategory, Revenue, Expense


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
        wallet_model = Wallet.objects.get(id=pk)
        if not request.method == "POST":

            context = {
                "wallet": wallet_model
            }
            return render(request, 'add_wallet.html', context)
        else:
            name = request.POST.get("name", None)
            description = request.POST.get("description", None)

            if not name:
                messages.error(request, "Nome da certeira é necessário")
                return render(request, "add_wallet.html", {})
            
            wallet_model.name = name
            wallet_model.description = description
            wallet_model.save()
            return wallet(request)
    
    user_wallets = Wallet.objects.filter(user_id=user_id)
    context = {
        "wallets": user_wallets
    }

    return render(request, 'wallet.html', context)

@login_required()
def delete_wallet(request: HttpRequest, pk = None):

    if not pk:
        messages.error(request, "O ID da carteira é necessário")
        return redirect("wallet")
    
    wallet = Wallet.objects.get(id=pk)
    if not wallet:
        messages.error(request, "Wallet não existe ou ID inválido!")
        return redirect("wallet")
    
    wallet.delete()
    return redirect("wallet")

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
            return redirect("wallet")

        wallet.save()
        return redirect("wallet")
        
    else:
        return render(request, 'add_wallet.html', {})

@login_required()
def transactions(request: HttpRequest, pk = None):
    user_id = request.user.id

    if pk:
        revenue = None
        expense = None

        try:
            revenue = Revenue.objects.get(id=pk)
        except:
            expense = Expense.objects.get(id=pk)

        if not request.method == "POST":
            context = {}
            context["wallets"] = Wallet.objects.filter(user_id=user_id)
            if revenue:
                context["transaction"] = revenue
            else:
                context["transaction"] = expense
            
            return render(request, "add_transaction.html", context)
        
        else:
            name = request.POST.get("name", None)
            value = request.POST.get("value", None)
            wallet_id = request.POST.get("wallet_id", None)
            recurring = request.POST.get("recurring", None)
            category_id = request.POST.get("category_id", None)
            date = request.POST.get("date", None)

            if not name:
                messages.error(request, "O nome da transferência é necessário")
                return redirect("transactions")
            
            if not value:
                messages.error(request, "O valor da transferência é necessário")
                return redirect("transactions")
            
            if not wallet_id:
                messages.error(request, "A carteira da transferência é necessária")
                return redirect("transactions")
            
            if not category_id:
                messages.error(request, "A categoria da transferência é necessária")
                return redirect("transactions")
            
            if not date:
                messages.error(request, "A data da transferência é necessária")
                return redirect("transactions")
            
            recurring = bool(int(recurring))

            if revenue:
                revenue.name = name
                revenue.value = value
                revenue.wallet_id = Wallet.objects.get(id=wallet_id)
                revenue.recurring = recurring
                revenue.category_id = RevenueCategory.objects.get(id=category_id)
                revenue.date = date
                revenue.save()
            else:
                expense.name = name
                expense.value = value
                expense.wallet_id = Wallet.objects.get(id=wallet_id)
                expense.recurring = recurring
                expense.category_id = ExpenseCategory.objects.get(id=category_id)
                expense.date = date
                expense.save()

            return transactions(request)

    expenses = Expense.objects.filter(user_id=user_id)
    revenues = Revenue.objects.filter(user_id=user_id)

    context = {
        "expenses": expenses,
        "revenues": revenues
    }

    return render(request, 'transactions.html', context)

@login_required()
def add_transaction(request: HttpRequest):

    if request.method == "POST":
        name = request.POST.get("name", None)
        value = request.POST.get("value", None)
        wallet_id = request.POST.get("wallet_id", None)
        recurring = request.POST.get("recurring", None)
        category_id = request.POST.get("category_id", None)
        date = request.POST.get("date", None)
        is_expense = request.POST.get("type", None)
        is_revenue = request.POST.get("type", None)

        if not name:
            messages.error(request, "O nome da transferência é necessário")
            return redirect("transactions")
            
        if not value:
            messages.error(request, "O valor da transferência é necessário")
            return redirect("transactions")
        
        if not wallet_id:
            messages.error(request, "A carteira da transferência é necessária")
            return redirect("transactions")
        
        if not category_id:
            messages.error(request, "A categoria da transferência é necessária")
            return redirect("transactions")
        
        if not date:
            messages.error(request, "A data da transferência é necessária")
            return redirect("transactions")
        
        recurring = bool(int(recurring))

        if is_revenue:
            revenue = Revenue(
                user_id = request.user,
                name = name,
                value = value,
                wallet_id = Wallet.objects.get(id=wallet_id),
                recurring = recurring,
                category_id = RevenueCategory.objects.get(id=category_id),
                date = date
            )
            revenue.save()

        if is_expense:
            expense = Expense(
                user_id = request.user,
                name = name,
                value = value,
                wallet_id = Wallet.objects.get(id=wallet_id),
                recurring = recurring,
                category_id = RevenueCategory.objects.get(id=category_id),
                date = date
            )
            expense.save()

        return transactions(request)
    else:
        return render(request, 'add_transaction.html', {})
    
@login_required
def delete_transaction(request: HttpRequest, pk = None):

    if not pk:
        messages.error(request, "O ID da transação é necessário")
        return redirect("transactions")
    
    revenue = None
    expense = None
    
    try:
        revenue = Revenue.objects.get(id=pk)
    except:
        expense = Expense.objects.get(id=pk)
    
    if revenue:
        revenue.delete()
    else:
        expense.delete()

    return redirect("transactions")

@login_required()
def categorys(request: HttpRequest, pk = None):
    user_id = request.user.id

    if pk:
        revenue_category = None
        expense_category = None
        try:
            revenue_category = RevenueCategory.objects.get(id=pk)
        except:
            expense_category = ExpenseCategory.objects.get(id=pk)

        if not request.method == "POST":
            context = {}
            if revenue_category:
                context["category"] = revenue_category
            else:
                context["category"] = expense_category
            
            return render(request, "add_category.html", context)
        
        else:
            name = request.POST.get("name", None)
            description = request.POST.get("description", None)
            essential = request.POST.get("essential", None)
            is_expense = request.POST.get("expense", None)
            is_revenue = request.POST.get("revenue", None)
            print(essential)

            if not name:
                messages.error(request, "O nome da categoria é necessário")
                return redirect("categorys")
            
            if not essential:
                messages.error(request, "É essencial informar se é uma categoria essencial ou não")
                return redirect("categorys")
        
            essential = bool(int(essential))
            print(essential)

            if revenue_category:
                revenue_category.name = name
                revenue_category.description = description
                revenue_category.essential = essential
                revenue_category.save()
            else:
                expense_category.name = name
                expense_category.description = description
                expense_category.essential = essential
                expense_category.save()
            return categorys(request)

    expense_categorys = ExpenseCategory.objects.filter(user_id=user_id)
    revenue_categorys = RevenueCategory.objects.filter(user_id=user_id)

    context = {
        "expense_categorys": expense_categorys,
        "revenue_categorys": revenue_categorys
    }
    return render(request, 'categorys.html', context)

@login_required()
def add_categorys(request: HttpRequest):

    if request.method == "POST":
        name = request.POST.get("name", None)
        description = request.POST.get("description", None)
        essential = request.POST.get("essential", None)
        is_expense = request.POST.get("expense", None)
        is_revenue = request.POST.get("revenue", None)

        if not name:
            messages.error(request, "O nome da categoria é necessário")
            return redirect("categorys")
        
        if not essential:
            messages.error(request, "É essencial informar se é uma categoria essencial ou não")
            return redirect("categorys")
        
        essential = bool(int(essential))

        if is_revenue:
            revenue_category = RevenueCategory(
                user_id = request.user,
                name = name,
                essential = essential,
                description = description
            )
            revenue_category.save()

        if is_expense:
            expense_category = ExpenseCategory(
                user_id = request.user,
                name = name,
                essential = essential,
                description = description
            )
            expense_category.save()

        return categorys(request)
    else:
        return render(request, 'add_category.html', {})
    
@login_required()
def delete_categorys(request: HttpRequest, pk = None):

    if not pk:
        messages.error(request, "O ID da categoria é necessário")
        return redirect("categorys")
    
    revenue_category = None
    expense_category = None
    
    try:
        revenue_category = RevenueCategory.objects.get(id=pk)
    except:
        expense_category = ExpenseCategory.objects.get(id=pk)
    
    if revenue_category:
        revenue_category.delete()
    else:
        expense_category.delete()

    return redirect("categorys")

@login_required()
def reports(request: HttpRequest):
    return render(request, 'reports.html', {})

@login_required()
def add_report(request: HttpRequest):
    if request.method == "POST":
        return render(request, 'add_report.html', {})
    else:
        return render(request, 'add_report.html', {})