from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('categorys/', views.categorys, name='categorys'),
    path('categorys/<uuid:pk>/', views.categorys, name='categorys'),
    path('categorys/<uuid:pk>/delete/', views.delete_categorys, name='delete_categorys'),
    path('categorys/add/', views.add_categorys, name='add_categorys'),

    path('wallet/', views.wallet, name='wallet'),
    path('wallet/<uuid:pk>/', views.wallet, name='wallet'),
    path('wallet/<uuid:pk>/delete/', views.delete_wallet, name='delete_wallet'),
    path('wallet/add/', views.add_wallet, name='add_wallet'),

    path('report/', views.reports, name='report'),
    path('report/add', views.add_report, name='add_report'),

    path('transactions/', views.transactions, name='transactions'),
    path('transactions/<str:input_type>/<uuid:pk>/', views.add_transaction, name='transaction'),
    path('transactions/<uuid:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/add', views.add_transaction, name='add_transaction'),
    path('transactions/add/<str:input_type>/', views.add_transaction, name='add_transaction'),
]