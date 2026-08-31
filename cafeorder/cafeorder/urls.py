from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from cafe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Employees CRUD
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/register/', views.employee_register, name='employee_register'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    # Shift Slots CRUD
    path('shift-slots/', views.shiftslot_list, name='shiftslot_list'),
    path('shift-slots/add/', views.shiftslot_create, name='shiftslot_create'),
    path('shift-slots/<int:pk>/edit/', views.shiftslot_update, name='shiftslot_update'),
    path('shift-slots/<int:pk>/delete/', views.shiftslot_delete, name='shiftslot_delete'),

    # Roster / Shifts CRUD
    path('roster/', views.roster, name='roster'),
    path('roster/add/', views.shift_create, name='shift_create'),
    path('roster/<int:pk>/edit/', views.shift_update, name='shift_update'),
    path('roster/<int:pk>/delete/', views.shift_delete, name='shift_delete'),

    # Attendance CRUD & Clocking
    path('attendance/clock-in/', views.clock_in, name='clock_in'),
    path('attendance/clock-out/', views.clock_out, name='clock_out'),
    path('attendance/my/', views.my_attendance, name='my_attendance'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/<int:pk>/edit/', views.attendance_update, name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),

    # Leave Requests CRUD & Approvals
    path('leave/apply/', views.leave_request_create, name='leave_request_create'),
    path('leave/my/', views.my_leave_requests, name='my_leave_requests'),
    path('leave/<int:pk>/cancel/', views.leave_cancel, name='leave_cancel'),
    path('leave/approvals/', views.leave_approval_list, name='leave_approval_list'),
    path('leave/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('leave/<int:pk>/reject/', views.leave_reject, name='leave_reject'),

    # Calculation Process / Payroll Report
    path('payroll/', views.payroll_summary, name='payroll_summary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)