from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
import datetime

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


# ---------- Dashboard & Overview ----------

@login_required
def dashboard(request):
    today = timezone.localdate()
    user_is_mgr = is_admin_or_manager(request.user)

    # Common metrics for user
    today_attendance = Attendance.objects.filter(employee=request.user, date=today).first()
    my_shifts = Shift.objects.filter(employee=request.user, date__gte=today).order_by('date')[:5]
    my_leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-start_date')[:5]
    
    # Calculate user's hours & earnings
    try:
        profile = request.user.employeeprofile
        user_total_hours = profile.get_total_hours_worked()
        user_total_earnings = profile.get_total_earnings()
        leave_balance = profile.leave_balance
    except EmployeeProfile.DoesNotExist:
        profile = None
        user_total_hours = 0.0
        user_total_earnings = 0.0
        leave_balance = 14

    context = {
        "today": today,
        "is_manager": user_is_mgr,
        "today_attendance": today_attendance,
        "my_shifts": my_shifts,
        "my_leaves": my_leaves,
        "user_total_hours": user_total_hours,
        "user_total_earnings": user_total_earnings,
        "leave_balance": leave_balance,
    }

    if user_is_mgr:
        # Management metrics
        total_employees = User.objects.count()
        today_shifts = Shift.objects.filter(date=today)
        active_clocked_in = Attendance.objects.filter(date=today, clock_out_time__isnull=True).count()
        pending_leaves_count = LeaveRequest.objects.filter(status="pending").count()
        pending_leaves = LeaveRequest.objects.filter(status="pending")[:5]

        context.update({
            "total_employees": total_employees,
            "today_shifts": today_shifts,
            "active_clocked_in": active_clocked_in,
            "pending_leaves_count": pending_leaves_count,
            "pending_leaves": pending_leaves,
        })

    return render(request, "dashboard.html", context)


# ---------- Employees (CRUD) ----------

@login_required
def employee_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("dashboard")
    employees = User.objects.all().select_related('employeeprofile')
    return render(request, "employee_list.html", {"employees": employees})


@login_required
def employee_register(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to register employees.")
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            EmployeeProfile.objects.create(user=new_user)
            messages.success(request, f"Employee account for '{new_user.username}' created. Now configure rate & role.")
            return redirect("employee_update", pk=new_user.pk)
    else:
        form = UserRegisterForm()
    return render(request, "employee_register.html", {"form": form})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(User, pk=pk)

    if not is_admin_or_manager(request.user) and request.user.pk != employee.pk:
        messages.error(request, "You are not allowed to edit other workers' information.")
        return redirect("dashboard")

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
            messages.success(request, f"Employee details for {employee.username} updated.")
            return redirect("employee_list" if is_admin_or_manager(request.user) else "dashboard")
    else:
        user_form = UserUpdateForm(instance=employee)
        profile_form = EmployeeProfileForm(instance=profile)

    return render(request, "employee_form.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "employee": employee,
    })


@login_required
def employee_delete(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to delete employees.")
        return redirect("dashboard")

    employee = get_object_or_404(User, pk=pk)
    if employee.pk == request.user.pk:
        messages.error(request, "You cannot delete your own account.")
        return redirect("employee_list")

    if request.method == "POST":
        username = employee.username
        employee.delete()
        messages.success(request, f"Employee '{username}' was successfully deleted.")
    return redirect("employee_list")


# ---------- Shift Slots (CRUD) ----------

@login_required
def shiftslot_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("dashboard")
    slots = ShiftSlot.objects.all()
    return render(request, "shiftslot_list.html", {"slots": slots})


@login_required
def shiftslot_create(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to add shift slots.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ShiftSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift slot added successfully.")
            return redirect("shiftslot_list")
    else:
        form = ShiftSlotForm()
    return render(request, "shiftslot_form.html", {"form": form})


@login_required
def shiftslot_update(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to edit shift slots.")
        return redirect("dashboard")

    slot = get_object_or_404(ShiftSlot, pk=pk)
    if request.method == "POST":
        form = ShiftSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift slot updated.")
            return redirect("shiftslot_list")
    else:
        form = ShiftSlotForm(instance=slot)
    return render(request, "shiftslot_form.html", {"form": form, "slot": slot})


@login_required
def shiftslot_delete(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to delete shift slots.")
        return redirect("dashboard")

    slot = get_object_or_404(ShiftSlot, pk=pk)
    if request.method == "POST":
        slot.delete()
        messages.success(request, "Shift slot deleted.")
    return redirect("shiftslot_list")


# ---------- Roster & Shifts (CRUD) ----------

@login_required
def roster(request):
    shifts = Shift.objects.all().select_related('employee', 'slot').order_by('date', 'slot__start_time')
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
            messages.success(request, "Shift scheduled successfully.")
            return redirect("roster")
    else:
        form = ShiftForm(initial={"date": timezone.localdate()})
    return render(request, "shift_form.html", {"form": form})


@login_required
def shift_update(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to edit shifts.")
        return redirect("roster")

    shift = get_object_or_404(Shift, pk=pk)
    if request.method == "POST":
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            messages.success(request, "Shift updated.")
            return redirect("roster")
    else:
        form = ShiftForm(instance=shift)
    return render(request, "shift_form.html", {"form": form, "shift": shift})


@login_required
def shift_delete(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to delete shifts.")
        return redirect("roster")

    shift = get_object_or_404(Shift, pk=pk)
    if request.method == "POST":
        shift.delete()
        messages.success(request, "Shift cancelled and removed from roster.")
    return redirect("roster")


# ---------- Attendance (CRUD & Clock Operations) ----------

@login_required
def clock_in(request):
    today = timezone.localdate()
    now_time = timezone.localtime().time()

    existing = Attendance.objects.filter(employee=request.user, date=today).first()

    if existing:
        messages.info(request, "You already have an active attendance record for today.")
    else:
        Attendance.objects.create(employee=request.user, date=today, clock_in_time=now_time)
        messages.success(request, f"Clocked in successfully at {now_time.strftime('%I:%M %p')}.")

    return redirect("dashboard")


@login_required
def clock_out(request):
    today = timezone.localdate()
    record = Attendance.objects.filter(employee=request.user, date=today).first()

    if not record:
        messages.error(request, "You have not clocked in today.")
    elif record.clock_out_time:
        messages.info(request, "You already clocked out today.")
    else:
        now_time = timezone.localtime().time()
        record.clock_out_time = now_time
        record.save()
        messages.success(request, f"Clocked out at {now_time.strftime('%I:%M %p')}. Total worked: {record.duration_formatted}.")

    return redirect("dashboard")


@login_required
def my_attendance(request):
    records = Attendance.objects.filter(employee=request.user).order_by('-date')
    total_hours = sum(r.hours_worked for r in records)
    return render(request, "my_attendance.html", {"records": records, "total_hours": round(total_hours, 2)})


@login_required
def attendance_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("dashboard")
    records = Attendance.objects.all().select_related('employee').order_by('-date', '-clock_in_time')
    return render(request, "attendance_list.html", {"records": records})


@login_required
def attendance_update(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to edit attendance records.")
        return redirect("dashboard")

    record = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, f"Attendance record for {record.employee.username} updated.")
            return redirect("attendance_list")
    else:
        form = AttendanceForm(instance=record)
    return render(request, "attendance_form.html", {"form": form, "record": record})


@login_required
def attendance_delete(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to delete attendance records.")
        return redirect("dashboard")

    record = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Attendance record removed.")
    return redirect("attendance_list")


# ---------- Leave Management (CRUD with Calculation Deduction) ----------

@login_required
def leave_request_create(request):
    try:
        profile = request.user.employeeprofile
        current_balance = profile.leave_balance
    except EmployeeProfile.DoesNotExist:
        current_balance = 14

    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            days = leave.total_days
            if days <= 0:
                messages.error(request, "Invalid dates: End date must be on or after start date.")
                return render(request, "leave_request_form.html", {"form": form, "current_balance": current_balance})
            
            leave.save()
            messages.success(request, f"Leave request for {days} day(s) submitted successfully.")
            return redirect("my_leave_requests")
    else:
        form = LeaveRequestForm()
    return render(request, "leave_request_form.html", {"form": form, "current_balance": current_balance})


@login_required
def my_leave_requests(request):
    requests = LeaveRequest.objects.filter(employee=request.user).order_by('-start_date')
    try:
        balance = request.user.employeeprofile.leave_balance
    except EmployeeProfile.DoesNotExist:
        balance = 14
    return render(request, "my_leave_requests.html", {"requests": requests, "leave_balance": balance})


@login_required
def leave_approval_list(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to view this page.")
        return redirect("dashboard")
    requests = LeaveRequest.objects.filter(status="pending").select_related('employee', 'employee__employeeprofile').order_by('start_date')
    return render(request, "leave_approval_list.html", {"requests": requests})


@login_required
def leave_approve(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to approve leave.")
        return redirect("dashboard")

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == "POST":
        days = leave.total_days
        try:
            profile = leave.employee.employeeprofile
            # Deduct leave days from balance
            profile.leave_balance = max(0, profile.leave_balance - days)
            profile.save()
            bal_msg = f"({days} days deducted, new balance: {profile.leave_balance} days)"
        except EmployeeProfile.DoesNotExist:
            bal_msg = ""

        leave.status = "approved"
        leave.save()
        messages.success(request, f"Leave request for {leave.employee.username} approved {bal_msg}.")
    return redirect("leave_approval_list")


@login_required
def leave_reject(request, pk):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to reject leave.")
        return redirect("dashboard")

    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == "POST":
        leave.status = "rejected"
        leave.save()
        messages.success(request, f"Leave request for {leave.employee.username} has been rejected.")
    return redirect("leave_approval_list")


@login_required
def leave_cancel(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, employee=request.user)
    if leave.status == "pending":
        if request.method == "POST":
            leave.delete()
            messages.success(request, "Your pending leave request has been cancelled.")
    else:
        messages.error(request, "Only pending leave requests can be cancelled.")
    return redirect("my_leave_requests")


# ---------- Calculation Module (Payroll & Wage Summary) ----------

@login_required
def payroll_summary(request):
    if not is_admin_or_manager(request.user):
        messages.error(request, "You are not allowed to access Payroll Reports.")
        return redirect("dashboard")

    users = User.objects.all().select_related('employeeprofile')
    payroll_data = []
    total_store_hours = 0.0
    total_store_payout = 0.0

    for u in users:
        try:
            prof = u.employeeprofile
            rate = float(prof.hourly_rate)
            bal = prof.leave_balance
            role = prof.get_role_display()
        except EmployeeProfile.DoesNotExist:
            rate = 0.0
            bal = 14
            role = "Staff"

        # Calculate attendance hours
        records = u.attendance_set.all()
        hours = sum(r.hours_worked for r in records)
        
        # Calculate regular and overtime (hours > 40 standard)
        regular_hours = min(hours, 40.0)
        ot_hours = max(0.0, hours - 40.0)
        
        base_pay = regular_hours * rate
        ot_pay = ot_hours * (rate * 1.5)
        gross_pay = base_pay + ot_pay

        total_store_hours += hours
        total_store_payout += gross_pay

        payroll_data.append({
            "user": u,
            "role": role,
            "rate": rate,
            "total_hours": round(hours, 2),
            "regular_hours": round(regular_hours, 2),
            "ot_hours": round(ot_hours, 2),
            "base_pay": round(base_pay, 2),
            "ot_pay": round(ot_pay, 2),
            "gross_pay": round(gross_pay, 2),
            "leave_balance": bal,
        })

    return render(request, "payroll_summary.html", {
        "payroll_data": payroll_data,
        "total_store_hours": round(total_store_hours, 2),
        "total_store_payout": round(total_store_payout, 2),
    })