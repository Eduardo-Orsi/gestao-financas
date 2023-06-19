from django.contrib import admin
from . import models

models_to_register = [
    models.Expense,
    models.ExpenseCategory,
    models.Revenue,
    models.RevenueCategory,
    models.Wallet
]

admin.site.register(models_to_register)
