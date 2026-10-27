from django.db import models
from apps.catalog.models import Product
from config import settings


# Create your models here.

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','product')


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending','Kutilmoqda'),
        ('confirmed','Tasdiqlangan'),
        ('delivering','Yetkazilmoqda'),
        ('completed','Yakunlangan'),
        ('canceled','Bekor qilingan')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    total = models.DecimalField(max_digits=14,decimal_places=0,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12,decimal_places=0)

    @property
    def line_total(self):
        return self.price * self.quantity


