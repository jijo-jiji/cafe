from django.db import models
from django.contrib.auth.models import User


class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin/Owner"),
        ("manager", "Store Manager"),
        ("staff", "Staff"),
    ]
    EMPLOYMENT_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("casual", "Casual"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="staff")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default="part_time")
    phone = models.CharField(max_length=30, blank=True)
    emergency_contact = models.CharField(max_length=150, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cert_expiry_date = models.DateField(null=True, blank=True)
    leave_balance = models.IntegerField(default=14)

    def __str__(self):
        return self.user.username


class ShiftSlot(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class Shift(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ShiftSlot, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    def __str__(self):
        return self.employee.username + " - " + str(self.date)


class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    clock_in_time = models.TimeField(null=True, blank=True)
    clock_out_time = models.TimeField(null=True, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.employee.username + " - " + str(self.date)


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ("annual", "Annual"),
        ("medical", "Medical"),
        ("emergency", "Emergency"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.employee.username + " - " + self.leave_type