from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from cafe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='order_list', permanent=False)),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Workers
    path("workers/register/", views.worker_register, name="worker_register"),
    path("workers/", views.worker_list, name="worker_list"),
    path("workers/<int:pk>/edit/", views.worker_update, name="worker_update"),

    # Menu items
    path("menu/", views.menu_item_list, name="menu_item_list"),
    path("menu/add/", views.menu_item_create, name="menu_item_create"),
    path("menu/<int:pk>/edit/", views.menu_item_update, name="menu_item_update"),
    path("menu/<int:pk>/delete/", views.menu_item_delete, name="menu_item_delete"),
    path("menu/<int:pk>/toggle/", views.menu_item_toggle_availability, name="menu_item_toggle_availability"),

    # Orders
    path("orders/", views.order_list, name="order_list"),
    path("orders/new/", views.order_create, name="order_create"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/add-item/", views.order_item_add, name="order_item_add"),
    path("orders/<int:pk>/remove-item/<int:item_pk>/", views.order_item_remove, name="order_item_remove"),
    path("orders/<int:pk>/status/", views.order_status_update, name="order_status_update"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)