from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
                                                                                                                                                                   

class MenuItem(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (RM {self.price})"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    table_number = models.CharField(max_length=20, blank=True)
    customer_name = models.CharField(max_length=150, blank=True)
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        label = self.customer_name or self.table_number or f"Order #{self.pk}"
        return f"{label} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse("order_detail", args=[self.pk])

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    note = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity