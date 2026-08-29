from django.contrib import admin
from .models import EmployeeProfile, ShiftSlot, Shift, Attendance, LeaveRequest

admin.site.register(EmployeeProfile)
admin.site.register(ShiftSlot)
admin.site.register(Shift)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)