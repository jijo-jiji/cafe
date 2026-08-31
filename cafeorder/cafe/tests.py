import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import EmployeeProfile, ShiftSlot, Shift, Attendance, LeaveRequest


class CafeHRMSTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Manager user
        self.manager_user = User.objects.create_user(
            username="manager_test",
            password="password123",
            first_name="Store",
            last_name="Manager"
        )
        self.manager_profile, _ = EmployeeProfile.objects.get_or_create(
            user=self.manager_user,
            defaults={"role": "manager", "hourly_rate": 20.00, "leave_balance": 14}
        )
        self.manager_profile.role = "manager"
        self.manager_profile.hourly_rate = 20.00
        self.manager_profile.save()

        # Staff user
        self.staff_user = User.objects.create_user(
            username="staff_test",
            password="password123",
            first_name="Cafe",
            last_name="Barista"
        )
        self.staff_profile, _ = EmployeeProfile.objects.get_or_create(
            user=self.staff_user,
            defaults={"role": "staff", "hourly_rate": 15.00, "leave_balance": 14}
        )

        # Shift slot
        self.slot = ShiftSlot.objects.create(
            name="Morning Roast",
            start_time=datetime.time(8, 0),
            end_time=datetime.time(16, 0)
        )

    def test_attendance_duration_calculation(self):
        """Test working hours computation between clock-in and clock-out."""
        att = Attendance.objects.create(
            employee=self.staff_user,
            date=datetime.date.today(),
            clock_in_time=datetime.time(8, 0),
            clock_out_time=datetime.time(16, 30)
        )
        # 8h 30m = 8.5 hours
        self.assertEqual(att.hours_worked, 8.5)
        self.assertEqual(att.duration_formatted, "8h 30m")

    def test_employee_total_earnings(self):
        """Test total earnings computation based on total attendance hours."""
        Attendance.objects.create(
            employee=self.staff_user,
            date=datetime.date(2026, 8, 1),
            clock_in_time=datetime.time(8, 0),
            clock_out_time=datetime.time(18, 0) # 10 hours
        )
        self.assertEqual(self.staff_profile.get_total_hours_worked(), 10.0)
        # 10 hrs * RM 15.00 = RM 150.00
        self.assertEqual(self.staff_profile.get_total_earnings(), 150.0)

    def test_leave_day_calculation_and_balance_deduction(self):
        """Test leave total days computation and automatic balance deduction on approval."""
        leave = LeaveRequest.objects.create(
            employee=self.staff_user,
            leave_type="annual",
            start_date=datetime.date(2026, 9, 1),
            end_date=datetime.date(2026, 9, 3), # 3 days inclusive
            reason="Vacation"
        )
        self.assertEqual(leave.total_days, 3)

        # Login as manager and approve leave
        self.client.login(username="manager_test", password="password123")
        response = self.client.post(f"/leave/{leave.pk}/approve/", follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify status and deducted balance
        leave.refresh_from_db()
        self.assertEqual(leave.status, "approved")
        self.staff_profile.refresh_from_db()
        self.assertEqual(self.staff_profile.leave_balance, 11) # 14 - 3 = 11

    def test_manager_access_control(self):
        """Test that regular staff cannot access sensitive manager endpoints."""
        self.client.login(username="staff_test", password="password123")
        
        # Staff attempting to access employee list or payroll should be redirected
        resp_emp = self.client.get("/employees/")
        self.assertEqual(resp_emp.status_code, 302)

        resp_payroll = self.client.get("/payroll/")
        self.assertEqual(resp_payroll.status_code, 302)

    def test_dashboard_renders_for_both_roles(self):
        """Test that dashboard renders HTTP 200 for both manager and staff."""
        self.client.login(username="manager_test", password="password123")
        resp_mgr = self.client.get("/")
        self.assertEqual(resp_mgr.status_code, 200)

        self.client.login(username="staff_test", password="password123")
        resp_staff = self.client.get("/")
        self.assertEqual(resp_staff.status_code, 200)
