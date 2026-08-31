# ☕ Cafe HRMS (Human Resource Management System)

> **Universiti Kuala Lumpur (UniKL MIIT)**  
> **Course:** Emerging Trend in Software Engineering (ISB 46203)  
> **Weightage:** 40% Project Assessment  
> **Domain:** Management Systems (Food & Beverage / Cafe Operations)

---

## 📖 Overview

**Cafe HRMS** is a full-stack web application developed using **Python** and the **Django Framework** following the **Model-View-Template (MVT)** architectural pattern. It is specifically tailored for cafe and F&B operations to streamline employee management, shift rostering, time-tracking attendance, annual/medical leave approvals, and automated payroll computations.

---

## ✨ Key System Features

### 1. 👥 Multi-Role Authorization
- **👑 Store Manager / Admin:**
  - Full CRUD operations on Employee Profiles, Shift Slots, Roster Schedules, and Attendance Records.
  - Review and approve/reject staff leave applications with automatic balance deduction.
  - Store-wide **Payroll Calculation Report** with total hours, overtime breakdown, and wage payouts.
- **☕ Cafe Staff / Barista:**
  - Personalized Dashboard with live shift statuses and duty notes.
  - One-click **Clock In** and **Clock Out** daily attendance recording.
  - View upcoming shifts on the store roster.
  - Submit leave requests with live day calculation and track remaining leave balances.
  - View personal logged hours and estimated wage earnings.

### 2. 🧮 Automated Calculation Process (Rubric-Compliant)
- **Work Duration Calculation:** Automatic computation of shift hours worked between clock-in and clock-out timestamps.
- **Overtime Wage Engine:** Computes overtime wages using the Malaysian standard multiplier (1.5x hourly rate) for weekly hours exceeding 40 hours:
  $$\text{Gross Pay} = (\text{Regular Hours} \times \text{Rate}) + (\text{Overtime Hours} \times \text{Rate} \times 1.5)$$
- **Leave Balance Engine:** Automatic duration computation and dynamic balance deduction upon manager approval.
- **Interactive Real-Time Estimator:** Client-side salary estimator widget embedded on the Payroll page.

### 3. 🎨 Modern Artisan UI & Interactive JavaScript
- **Custom CSS Design System (`style.css`):** Warm Artisan Espresso (`#2d1a12`) and Caramel Amber (`#d97706`) theme with Google Fonts (*Inter* & *Outfit*), KPI summary metric cards, role badges, and zebra-striped tables.
- **Interactive JavaScript (`main.js`):**
  - Live real-time digital clock on the top navbar.
  - Instant client-side table search & filtering (no page reloads).
  - Dynamic leave day calculator with balance validation.
  - Confirmation modals for delete and cancellation actions.
  - Auto-dismissing notification toasts.

---

## 🏗️ Architecture & Modules (MVT)

```
cafe/
├── README.md                  # Project Documentation
├── PROJECT (40%).pdf          # UniKL Assessment Brief
└── cafeorder/                 # Django Root Directory
    ├── manage.py              # CLI Utility Runner
    ├── db.sqlite3             # Relational Database Storage
    ├── cafeorder/             # Project Configuration
    │   ├── settings.py        # Settings, Static & Auth
    │   ├── urls.py            # Global URL Routing
    │   └── wsgi.py / asgi.py  # Server Gateways
    ├── cafe/                  # Core HRMS App
    │   ├── models.py          # Relational Data Models & Calculations
    │   ├── views.py           # Business Logic, Controllers & Permissions
    │   ├── forms.py           # ModelForms with StyledFormMixin
    │   ├── tests.py           # Automated Unit Test Suite
    │   └── templates/         # HTML5 Presentation Templates
    └── static/                # Static Asset Design Tokens
        ├── css/style.css      # Cafe Theme Stylesheet
        ├── js/main.js         # Interactive Client JavaScript
        └── images/logo.svg    # Vector Branding Logo
```

---

## 🔑 Demo Accounts for Examination & Testing

| Role | Username | Password | Privileges |
| :--- | :--- | :--- | :--- |
| **Manager / Admin** | `admin` | `admin123` | Full access to employee directory, pay rates, shift roster, leave approvals, and payroll report. |
| **Barista / Staff** | `adam` | `adam123` | Clock-in/out, view personal attendance, view shifts, apply for leave. |
| **Senior Barista** | `sarah` | `sarah123` | Barista account with assigned shifts and pending leave request. |
| **Assistant Crew** | `haziq` | `haziq123` | Casual staff account. |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Django 5.x

### Setup & Run
```bash
# 1. Clone repository
git clone https://github.com/jijo-jiji/cafe.git
cd cafe/cafeorder

# 2. Run Database Migrations
python manage.py migrate

# 3. Start Development Server
python manage.py runserver
```

Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 🧪 Running Automated Tests

Run the full Django test suite verifying models, duration calculations, leave deductions, and access control:

```bash
python manage.py test
```

---

## 📄 Academic Project Report
The complete academic project report complying with all UniKL MIIT formatting requirements (Arial/Calibri, 1.5 line spacing, numbered canvas, cover page, business process screenshots, and MVT explanation) is generated as `CAFE_HRMS_PROJECT_REPORT.pdf`.

---

## 👥 Contributors (Group Members)
1. **Adam Haris bin Razak** (52213123001) - *Frontend UI/UX, CSS Theme & JavaScript*
2. **Sarah Lee Xiao Wei** (52213123002) - *Backend MVT Architecture, Models & Views*
3. **Haziq Danial bin Roslan** (52213123003) - *Calculation Engine, Testing & Documentation*
