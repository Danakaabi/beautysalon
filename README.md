
<img width="1536" height="1024" alt="Beauty Salon Management System - Final ERD" src="https://github.com/user-attachments/assets/f4d27bca-c570-48d0-b2cd-4e5134b9cbd3" />
<img width="1536" height="1024" alt="Beauty Salon Management System - Data Flow Diagram (DFD)" src="https://github.com/user-attachments/assets/eca84ae8-9920-415a-a375-478f28a502a9" />

# Beauty Salon Management System
## Project Documentation Report

---

# 1. Project Overview

The Beauty Salon Management System is a web-based application developed using Django to simplify appointment booking, service management, staff management, and customer operations within a beauty salon environment.

The system provides a complete customer booking workflow, beginning with authentication and ending with appointment confirmation, while maintaining a modular architecture that supports staff scheduling, notifications, billing, analytics, and future scalability.

The project follows a modular design approach by separating business domains into independent Django applications.

---

# 2. Project Objectives

The primary objectives of the system are:

- Simplify appointment booking for customers.
- Organize salon services and categories.
- Manage staff availability and service assignments.
- Reduce manual scheduling operations.
- Prevent booking conflicts.
- Provide a scalable salon management foundation.
- Support future integration with payment systems and SMS providers.
- Deliver a modern and responsive user experience.

---

# 3. Technology Stack

| Component | Technology |
|------------|------------|
| Backend | Django |
| Language | Python |
| Frontend | HTML, CSS, JavaScript |
| Templates | Django Templates |
| Database | SQLite (Development) |
| Authentication | OTP-Based Login |
| Session Management | Django Sessions |
| ORM | Django ORM |

---

# 4. System Architecture

```text
Beauty Salon Management System
│
├── accounts
├── bookings
├── catalog
├── scheduling
├── notifications_center
├── billing
├── portal_client
├── control_panel
│
├── templates
├── static
├── media
└── salon_project
```

This modular architecture improves maintainability, scalability, and separation of concerns.

---

# 5. Application Modules

## 5.1 Accounts Module

### Purpose

Manage customer authentication and account access.

### Responsibilities

- OTP generation
- OTP verification
- User authentication
- Session creation
- Customer dashboard access

### Main Components

```text
CustomUser
OTP
generate_otp()
verify_otp()
```

### Authentication Flow

```text
Customer enters phone number
            ↓
Generate OTP
            ↓
OTP Verification
            ↓
Login Success
            ↓
Customer Dashboard
```

---

## 5.2 Catalog Module

### Purpose

Manage salon services and categories.

### Models

#### ServiceCategory

```text
id
name
description
is_active
created_at
updated_at
```

#### Service

```text
id
category_id
name
description
price
duration_minutes
is_active
created_at
updated_at
```

### Responsibilities

```text
Service Management
Pricing Management
Service Categorization
Duration Management
```

---

## 5.3 Scheduling Module

### Purpose

Manage salon staff and service capabilities.

### Models

#### Staff

```text
id
name
phone
is_active
created_at
updated_at
```

#### StaffService

```text
id
staff_id
service_id
```

### Responsibilities

```text
Staff Management
Service Assignment
Availability Planning
Scheduling Foundation
```

---

## 5.4 Bookings Module

### Purpose

Handle appointment booking operations.

### Models

#### TimeSlot

```text
id
time
```

#### Booking

```text
id
user_id
date
time_id
staff_member_id
status
total_amount
notes
created_at
updated_at
```

### Status Values

```text
pending
confirmed
completed
canceled
no_show
```

#### BookingItem

```text
id
booking_id
service_id
price_at_booking
duration_at_booking
```

---

# 6. Booking Workflow

## Step 1 — Service Selection

```text
Customer
    ↓
Choose Service
```

## Step 2 — Date Selection

```text
Customer
    ↓
Choose Date
```

## Step 3 — Time Slot Selection

```text
Customer
    ↓
Choose Time Slot
```

## Step 4 — Booking Confirmation

Customer reviews:

```text
Service
Date
Time
Phone Number
```

## Step 5 — Booking Creation

```text
Booking
    ↓
BookingItem
```

Status:

```text
confirmed
```

## Step 6 — Booking Success Page

Displays:

```text
Booking Information
Service Details
Appointment Date
Appointment Time
```

---

# 7. Customer Portal

## Features

### Upcoming Appointment

Displays:

```text
Services
Date
Time
Status
Total Amount
```

### Actions

```text
Edit Booking
Cancel Booking
```

### Appointment History

Displays previous appointments.

---

# 8. Staff Portal

### Templates

```text
staff/base.html
staff/dashboard.html
staff/bookings.html
staff/profile.html
staff/schedule.html
staff/notifications.html
```

### Planned Features

```text
Assigned Appointments
Availability Management
Schedule Control
Notifications
Performance Tracking
```

---

# 9. Notifications Center

### Purpose

Centralized notification management.

### Planned Notifications

```text
Appointment Confirmation
Appointment Reminder
Booking Cancellation
Staff Notifications
Administrative Alerts
```

---

# 10. Billing Module

### Purpose

Manage payments and invoices.

### Future Features

```text
Invoice Generation
Online Payments
Payment Tracking
Transaction History
Refund Management
```

---

# 11. Control Panel

### Purpose

Administrative management.

### Planned Features

```text
Customer Management
Service Management
Category Management
Staff Management
Booking Management
Reports
Analytics
```

---

# 12. User Interface Design

### Design Characteristics

- RTL Arabic Support
- Mobile Friendly
- Responsive Layout
- Gradient-Based Design
- Glassmorphism Components
- Consistent Branding

### Primary Colors

```text
#5A00E6
#8A2BFF
#C77AFF
#F3CBFF
#00D5C3
```

---

# 13. Database Design

## Current Core Entities

```text
ServiceCategory
        │ 1
        │
        ▼
      Service
        ▲
        │
        │ M
   StaffService
        │
        ▼
      Staff

CustomUser
      │ 1
      │
      ▼
    Booking
      │ 1
      │
      ▼
  BookingItem
      │ M
      │
      ▼
    Service

Booking
    │ M
    │
    ▼
 TimeSlot
```

---

# 14. ERD

```text
CustomUser
-----------
id (PK)
phone
...

        1
        │
        ▼
Booking
-----------
id (PK)
user_id (FK)
date
time_id (FK)
staff_member_id (FK)
status
total_amount
notes
created_at
updated_at

        1
        │
        ▼
BookingItem
-----------
id (PK)
booking_id (FK)
service_id (FK)
price_at_booking
duration_at_booking

        M
        │
        ▼
Service
-----------
id (PK)
category_id (FK)
name
price
duration_minutes

        M
        │
        ▼
ServiceCategory
-----------
id (PK)
name

Staff
-----------
id (PK)
name
phone

        M
        │
        ▼
StaffService
-----------
id (PK)
staff_id (FK)
service_id (FK)

TimeSlot
-----------
id (PK)
time
```

---

# 15. Implemented Features

### Completed

✅ OTP Authentication (Development Mode)

✅ Service Categories

✅ Service Catalog

✅ Staff Management Foundation

✅ Staff-Service Assignment

✅ Service Selection

✅ Date Selection

✅ Time Selection

✅ Booking Confirmation

✅ Appointment Creation

✅ Booking Success Page

✅ Customer Dashboard

✅ Appointment History

✅ Booking Cancellation

✅ Appointment Editing

✅ BookingItem Architecture

✅ Total Amount Tracking

✅ Responsive User Interface

✅ Modular Django Architecture

---

# 16. Future Enhancements

## Authentication

- SMS Provider Integration
- OTP Expiration Logic
- Rate Limiting

## Booking

- Staff Selection
- Conflict Detection
- Multi-Service Booking UI
- Service Duration Validation

## Notifications

- SMS Reminders
- Email Notifications
- WhatsApp Integration

## Billing

- Payment Gateway Integration
- Invoice Generation

## Administration

- Advanced Analytics
- Reports Dashboard
- Branch Management

## Scalability

- PostgreSQL Migration
- Redis Caching
- REST API Development
- React Frontend
- Mobile Application Integration

---

# 17. Engineering Evaluation

### Current Project Classification

```text
Salon Management System
with
Appointment Booking Platform
```

### Project Maturity

```text
Frontend UI/UX        █████████░ 90%
Authentication        ███████░░░ 70%
Booking Workflow      ████████░░ 85%
Database Design       █████████░ 90%
Service Catalog       ████████░░ 85%
Staff Management      ██████░░░░ 60%
Notifications         ██░░░░░░░░ 20%
Billing               ██░░░░░░░░ 20%
Administration        ███░░░░░░░ 30%
```

### Overall Progress

```text
≈ 80% MVP Completion
```

---

# 18. Engineering Assessment

The project now demonstrates:

```text
Normalized Database Design
One-to-Many Relationships
Many-to-Many Relationships
Booking Aggregation Pattern
Price Snapshot Strategy
Modular Django Architecture
Session-Based Authentication
Responsive UI Design
Migration-Based Database Evolution
```

### Current Engineering Level

```text
Junior+ / Early Mid-Level Architecture
```

---

# 19. Conclusion

The Beauty Salon Management System has evolved from a simple appointment booking application into a structured salon management platform.

The current implementation supports customer authentication, service catalog management, staff-service assignment, appointment booking, booking history, and scalable database architecture.

The project is prepared for future expansion into advanced scheduling, conflict prevention, notifications, billing, analytics, REST APIs, React frontend integration, and mobile applications while maintaining a clean and maintainable Django architecture.
