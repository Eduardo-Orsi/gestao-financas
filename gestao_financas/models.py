from uuid import uuid4

from django.db import models

from users.models import UserProfile


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.name


class RevenueCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    essential = models.BooleanField()
    default = models.BooleanField(null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Revenue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    wallet_id = models.ForeignKey(to=Wallet, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    value = models.FloatField(null=False)
    recurring = models.BooleanField(default=False)
    category_id = models.ForeignKey(RevenueCategory, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ExpenseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    essential = models.BooleanField()
    default = models.BooleanField(null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    wallet_id = models.ForeignKey(to=Wallet, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    value = models.FloatField(null=False)
    recurring = models.BooleanField(default=False)
    category_id = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    