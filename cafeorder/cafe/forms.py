from django import forms
from .models import MenuItem, Category, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "category", "price", "is_available", "image"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number", "customer_name", "status"]

from django.forms import inlineformset_factory
from .models import Order, OrderItem

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=["menu_item", "quantity", "note"],
    extra=1,
    can_delete=True,
)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity", "note"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only show items currently available to order
        self.fields["menu_item"].queryset = MenuItem.objects.filter(is_available=True)


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]

class WorkerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active"]