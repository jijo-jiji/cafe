from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import MenuItem, Order, OrderItem
from .forms import MenuItemForm, OrderForm, OrderItemForm, OrderStatusForm
from .forms import OrderForm, OrderItemFormSet, WorkerUpdateForm,WorkerRegisterForm
from django.contrib.auth.models import User



# ---------- Menu items ----------

@login_required
def menu_item_list(request):
    items = MenuItem.objects.select_related("category").all()
    return render(request, "menu_item_list.html", {"items": items})


def admin_required(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_required)
def worker_list(request):
    workers = User.objects.all().order_by("username")
    return render(request, "worker_list.html", {"workers": workers})


@login_required
@user_passes_test(admin_required)
def worker_update(request, pk):
    worker = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = WorkerUpdateForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, "Worker details updated.")
            return redirect("worker_list")
    else:
        form = WorkerUpdateForm(instance=worker)
    return render(request, "worker_form.html", {"form": form, "title": f"Edit {worker.username}"})

@login_required
@user_passes_test(admin_required)
def worker_register(request):
    if request.method == "POST":
        form = WorkerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Worker account created.")
            return redirect("worker_register")
    else:
        form = WorkerRegisterForm()
    return render(request, "worker_form.html", {"form": form, "title": "Register Worker"})

@login_required
@user_passes_test(admin_required)
def worker_update(request, pk):
    worker = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = WorkerUpdateForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, "Worker details updated.")
            return redirect("worker_list")
    else:
        form = WorkerUpdateForm(instance=worker)
    return render(request, "worker_form.html", {"form": form, "title": f"Edit {worker.username}"})


@login_required
def menu_item_create(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added.")
            return redirect("menu_item_list")
    else:
        form = MenuItemForm()
    return render(request, "menu_item_form.html", {"form": form, "title": "Add Menu Item"})


@login_required
def menu_item_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated.")
            return redirect("menu_item_list")
    else:
        form = MenuItemForm(instance=item)
    return render(request, "menu_item_form.html", {"form": form, "title": "Edit Menu Item"})


@login_required
def menu_item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Menu item deleted.")
        return redirect("menu_item_list")
    return render(request, "/menu_item_confirm_delete.html", {"item": item})


# ---------- Orders ----------

@login_required
def order_list(request):
    orders = Order.objects.select_related("worker").prefetch_related("items__menu_item").all()
    return render(request, "order_list.html", {"orders": orders})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.worker = request.user
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, "Order created.")
            return redirect("order_detail", pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, "order_form.html", {"form": form, "formset": formset, "title": "New Order"})

@login_required
def menu_item_toggle_availability(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "POST":
        item.is_available = not item.is_available
        item.save()
        messages.success(request, f"{item.name} marked as {'available' if item.is_available else 'unavailable'}.")
    return redirect("menu_item_list")


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    item_form = OrderItemForm()
    status_form = OrderStatusForm(instance=order)
    return render(
        request,
        "order_detail.html",
        {
            "order": order,
            "item_form": item_form,
            "status_form": status_form,
        },
    )


@login_required
def order_item_add(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            messages.success(request, "Item added to order.")
    return redirect("order_detail", pk=order.pk)


@login_required
def order_item_remove(request, pk, item_pk):
    order = get_object_or_404(Order, pk=pk)
    order_item = get_object_or_404(OrderItem, pk=item_pk, order=order)
    if request.method == "POST":
        order_item.delete()
        messages.success(request, "Item removed from order.")
    return redirect("order_detail", pk=order.pk)


@login_required
def order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
    return redirect("order_detail", pk=order.pk) 