from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import EmployeeProfile, ShiftSlot, Shift, Attendance, LeaveRequest
from .forms import (
    UserRegisterForm, UserUpdateForm, EmployeeProfileForm,
    ShiftSlotForm, ShiftForm, AttendanceForm, LeaveRequestForm
)


def is_admin_or_manager(user):
    if user.is_superuser:
        return True
    try:
        return user.employeeprofile.role in ["admin", "manager"]
    except EmployeeProfile.DoesNotExist:
        return False


# ---------- Employees ----------

@login_required
def employee_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("my_attendance")
    employees = User.objects.all()
    return render(request, "employee_list.html", {"employees": employees})


@login_required
def employee_register(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to register employees.")
        return redirect("my_attendance")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            EmployeeProfile.objects.create(user=new_user)
            messages.success(request, "Employee account created. Now set their details.")
            return redirect("employee_update", pk=new_user.pk)
    else:
        form = UserRegisterForm()
    return render(request, "employee_register.html", {"form": form})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(User, pk=pk)

    # Workers can only edit their own profile, not other workers'
    if not is_admin_or_manager(request.user) and request.user.pk != employee.pk:
        messages.error(request, "You are not allowed to edit other workers' information.")
        return redirect("my_attendance")

    try:
        profile = employee.employeeprofile
    except EmployeeProfile.DoesNotExist:
        profile = EmployeeProfile.objects.create(user=employee)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=employee)
        profile_form = EmployeeProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Employee updated.")
            return redirect("employee_list")
    else:
        user_form = UserUpdateForm(instance=employee)
        profile_form = EmployeeProfileForm(instance=profile)

    return render(request, "employee_form.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "employee": employee,
    })


# ---------- Shift Slots ----------

@login_required
def shiftslot_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("my_attendance")
    slots = ShiftSlot.objects.all()
    return render(request, "shiftslot_list.html", {"slots": slots})


@login_required
def shiftslot_create(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to add shift slots.")
        return redirect("my_attendance")

    if request.method == "POST":
        form = ShiftSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift slot added.")
            return redirect("shiftslot_list")
    else:
        form = ShiftSlotForm()
    return render(request, "shiftslot_form.html", {"form": form})


# ---------- Roster / Shifts ----------

@login_required
def roster(request):
    # Everyone (including workers) can view the roster
    shifts = Shift.objects.all()
    return render(request, "roster.html", {"shifts": shifts})


@login_required
def shift_create(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to assign shifts.")
        return redirect("roster")

    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift added.")
            return redirect("roster")
    else:
        form = ShiftForm()
    return render(request, "shift_form.html", {"form": form})


# ---------- Attendance ----------

@login_required
def clock_in(request):
    today = timezone.localdate()
    now_time = timezone.localtime().time()

    existing = Attendance.objects.filter(employee=request.user, date=today).first()

    if existing:
        messages.info(request, "You already have an attendance record for today.")
    else:
        Attendance.objects.create(employee=request.user, date=today, clock_in_time=now_time)
        messages.success(request, "Clocked in.")

    return redirect("my_attendance")


@login_required
def clock_out(request):
    today = timezone.localdate()
    record = Attendance.objects.filter(employee=request.user, date=today).first()

    if not record:
        messages.error(request, "You have not clocked in today.")
    elif record.clock_out_time:
        messages.info(request, "You already clocked out today.")
    else:
        record.clock_out_time = timezone.localtime().time()
        record.save()
        messages.success(request, "Clocked out.")

    return redirect("my_attendance")


@login_required
def my_attendance(request):
    # Everyone can view their own attendance
    records = Attendance.objects.filter(employee=request.user)
    return render(request, "my_attendance.html", {"records": records})


@login_required
def attendance_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("my_attendance")
    records = Attendance.objects.all()
    return render(request, "attendance_list.html", {"records": records})


@login_required
def attendance_update(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to edit attendance records.")
        return redirect("my_attendance")

    record = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated.")
            return redirect("attendance_list")
    else:
        form = AttendanceForm(instance=record)
    return render(request, "attendance_form.html", {"form": form, "record": record})


# ---------- Leave ----------

@login_required
def leave_request_create(request):
    # Everyone can apply for their own leave
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, "Leave request submitted.")
            return redirect("my_leave_requests")
    else:
        form = LeaveRequestForm()
    return render(request, "leave_request_form.html", {"form": form})


@login_required
def my_leave_requests(request):
    # Everyone can view their own leave requests
    requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, "my_leave_requests.html", {"requests": requests})


@login_required
def leave_approval_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("my_attendance")
    requests = LeaveRequest.objects.filter(status="pending")
    return render(request, "leave_approval_list.html", {"requests": requests})


@login_required
def leave_approve(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to approve leave.")
        return redirect("my_attendance")

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == "POST":
        leave.status = "approved"
        leave.save()
        messages.success(request, "Leave approved.")
    return redirect("leave_approval_list")


@login_required
def leave_reject(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to reject leave.")
        return redirect("my_attendance")

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == "POST":
        leave.status = "rejected"
        leave.save()
        messages.success(request, "Leave rejected.")
    return redirect("leave_approval_list")