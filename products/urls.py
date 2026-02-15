from django.urls import path
from . import views

urlpatterns = [
    path("", views.billing_page, name="billing"),
    path("purchases/", views.customer_purchases, name="purchases"),
    path("purchase/<int:pk>/", views.purchase_detail, name="purchase_detail"),
]
