from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmployeeProfile, ShiftSlot, Shift, Attendance, LeaveRequest


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active"]


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["role", "employment_type", "phone", "emergency_contact", "hourly_rate", "cert_expiry_date", "leave_balance"]
        widgets = {
            "cert_expiry_date": forms.DateInput(attrs={"type": "date"}),
        }


class ShiftSlotForm(forms.ModelForm):
    class Meta:
        model = ShiftSlot
        fields = ["name", "start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["employee", "slot", "date", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["clock_in_time", "clock_out_time", "notes"]
        widgets = {
            "clock_in_time": forms.TimeInput(attrs={"type": "time"}),
            "clock_out_time": forms.TimeInput(attrs={"type": "time"}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }