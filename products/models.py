from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField()
    unit_price = models.FloatField(max_length=10)
    tax_percentage = models.FloatField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.product_id})"
    
class Purchase(models.Model):
    customer_email = models.EmailField()
    total_without_tax = models.FloatField(default=0)
    total_tax = models.FloatField(default=0)
    net_total = models.FloatField(default=0)
    rounded_total = models.FloatField(default=0)
    amount_paid = models.FloatField()
    balance_returned = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_email} - {self.created_at}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.FloatField()
    tax_amount = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class ShopDenomination(models.Model):
    value = models.IntegerField(unique=True)
    available_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.value} - {self.available_count}"