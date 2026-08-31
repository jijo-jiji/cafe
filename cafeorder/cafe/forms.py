from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmployeeProfile, ShiftSlot, Shift, Attendance, LeaveRequest


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs.update({"class": "form-select"})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-checkbox"})
            else:
                existing_class = field.widget.attrs.get("class", "")
                field.widget.attrs.update({"class": f"form-control {existing_class}".strip()})


class UserRegisterForm(StyledFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserUpdateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active"]


class EmployeeProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["role", "employment_type", "phone", "emergency_contact", "hourly_rate", "cert_expiry_date", "leave_balance"]
        widgets = {
            "cert_expiry_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hourly_rate": forms.NumberInput(attrs={"step": "0.50", "min": "0", "placeholder": "e.g. 15.00"}),
            "leave_balance": forms.NumberInput(attrs={"min": "0", "placeholder": "e.g. 14"}),
        }


class ShiftSlotForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ShiftSlot
        fields = ["name", "start_time", "end_time"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Morning Shift, Night Shift"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }


class ShiftForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["employee", "slot", "date", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class AttendanceForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["clock_in_time", "clock_out_time", "notes"]
        widgets = {
            "clock_in_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "clock_out_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "notes": forms.TextInput(attrs={"placeholder": "e.g. On-time, Covered extra shift"}),
        }


class LeaveRequestForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "reason": forms.Textarea(attrs={"rows": 3, "placeholder": "Reason for leave..."}),
        }