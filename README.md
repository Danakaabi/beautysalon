![Beauty Salon Management System - Final ERD](assets/Beauty%20Salon%20Management%20System%20-%20Final%20ERD.PNG)

![Beauty Salon Management System - Data Flow Diagram (DFD)](assets/Beauty%20Salon%20Management%20System%20-%20Data%20Flow%20Diagram%20(DFD).PNG)
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

Manage salon staff, availability, schedules, and service assignments.

### Models

#### Staff

```text
id
user_id
name
phone
is_active
created_at
updated_at

#### StaffService

```text
id
staff_id
service_id
```

### StaffAvailability

```text
id
staff_id
day_of_week
start_time
end_time
is_active
created_at
updated_at
```

### Responsibilities

```text
Staff Management
Staff Portal
Service Assignment
Availability Management
Schedule Management
Booking Execution
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

## Step 6 — Customer Journey 
# 6. Customer Journey

The system provides a complete end-to-end customer booking experience.

## Step 1 — Authentication

```text
Enter Phone Number
        ↓
Generate OTP
        ↓
Verify OTP
        ↓
Customer Login
```

## Step 2 — Service Selection

```text
Customer
        ↓
Select Service
```

## Step 3 — Staff Selection

```text
Customer
        ↓
Select Staff

OR

Any Available Staff
```

## Step 4 — Date Selection

```text
Customer
        ↓
Select Date
```

## Step 5 — Time Selection

```text
Customer
        ↓
Select Available Time Slot
```

## Step 6 — Booking Confirmation

Customer reviews:

```text
Service
Staff Member
Date
Time
Phone Number
Total Amount
```

## Step 7 — Booking Creation

```text
Booking
        ↓
BookingItem
        ↓
Price Calculation
```

Status:

```text
confirmed
```

## Step 8 — Success Page

Displays:

```text
Booking Reference
Service Details
Staff Details
Date
Time
Total Amount
```

## Step 9 — Customer Dashboard

Provides:

```text
Upcoming Appointments
Booking History
Edit Booking
Cancel Booking
```
---
# 10.Booking Engine 


The booking engine is responsible for validating appointments and ensuring scheduling consistency.

## Responsibilities

```text
Booking Creation
Booking Validation
Booking Editing
Booking Cancellation
Price Calculation
Staff Assignment
```

## Features

```text
Conflict Prevention
Duplicate Booking Detection
Staff Availability Validation
Booking History Tracking
Appointment Rescheduling
```
# 11. Customer Portal

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
# 12. Conflict Prevention Engine

One of the most important implemented features is preventing scheduling conflicts.

The system validates:

```text
Date
Time Slot
Staff Member
Booking Status
```

Before creating a booking.

## Example

```text
Amal
18-06-2026
11:00
```

If already booked:

```text
Booking Rejected
```

and the customer receives a validation message.

## Booked Slot Locking

Booked slots appear as:

```text
11:00 (Booked)
```

and cannot be selected again.

### Templates

# 13. Staff Portal

### Implemented Pages

```text
staff/dashboard.html
staff/bookings.html
staff/booking-detail.html
staff/profile.html
staff/schedule.html
staff/availability.html
staff/notifications.html
```
Implemented Features
Staff Dashboard
Today's Appointments
Booking Details
Start Service
Complete Service
Profile Management
Schedule View
Availability Management
Notifications Interface

URLs

/schedule/staff/dashboard/
/schedule/staff/bookings/
/schedule/staff/bookings/<id>/
/schedule/staff/profile/
/schedule/staff/schedule/
/schedule/staff/availability/
/schedule/staff/notifications/

### Planned Features

```text
Assigned Appointments
Availability Management
Schedule Control
Notifications
Performance Tracking
```

---

# 14. Notifications Center

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

# 15. Billing Module

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

# 16. Control Panel

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

# 16. User Interface Design

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

# 17. Database Design

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

 CustomUser
      │ 1
      │
      ▼
    Staff
      │ 1
      │
      ▼
StaffAvailability



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

```text

Staff

-----------

id (PK)

user_id (FK)

name

phone

is_active

        1

        │

        ▼

StaffAvailability

-----------

id (PK)

staff_id (FK)

day_of_week

start_time

end_time

is_active

---
# 18. Implemented Features

## Completed Features

✅ OTP Authentication

✅ Service Categories

✅ Service Catalog

✅ Staff Management Foundation

✅ Staff-Service Assignment

✅ Service Selection

✅ Staff Selection

✅ Automatic Staff Assignment

✅ Date Selection

✅ Time Selection

✅ Booking Confirmation

✅ Appointment Creation

✅ Booking Success Page

✅ Customer Dashboard

✅ Appointment History

✅ Appointment Cancellation

✅ Appointment Rescheduling

✅ Booking Update Without Record Duplication

✅ Duplicate Booking Prevention

✅ Conflict Detection

✅ Booked Slot Locking

✅ BookingItem Architecture

✅ Dynamic Price Calculation

✅ Total Amount Tracking

✅ Responsive User Interface

✅ Modular Django Architecture

 Staff Portal

✅ Staff Dashboard

✅ Staff Profile

✅ Staff Schedule

✅ Staff Availability Management

✅ Booking Details Page

✅ Service Start Workflow

✅ Service Completion Workflow

✅ Staff ↔ User Relationship

✅ Role-Based Access Control

✅ Protected Staff Pages
---

# 19. Staff Availability System

The Staff Availability System allows salon employees to define their working days and available booking hours.

### Model

```text
StaffAvailability

Features
Working Day Definition
Availability Tracking
Schedule Visibility
Future Booking Validation Support

Example
Sunday
09:00 → 17:00

Monday
09:00 → 17:00

Tuesday
09:00 → 17:00

Future Integration
Prevent Booking Outside Working Hours
Available Slot Generation
Automatic Schedule Validation


# 20. Future Enhancements

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
# 21. Engineering Evaluation

### Current Project Classification

```text
Salon Management System

with

Appointment Booking Platform

Customer Self-Service Portal

Staff Scheduling Foundation
```

### Project Maturity
```
Frontend UI/UX        ███████████████████░   95%
Authentication        ██████████████████░░   90%
Booking Workflow      ████████████████████  100%
Database Design       ███████████████████░   95%
Service Catalog       ███████████████████░   95%
Staff Portal          ████████████████████  100%
Staff Availability    ████████████████████  100%
Notifications         █████░░░░░░░░░░░░░░   25%
Billing               ████░░░░░░░░░░░░░░░   20%
Administration        ███████░░░░░░░░░░░░   35%
Analytics             ██░░░░░░░░░░░░░░░░░   10%
```

### Overall Progress

```text
≈ ≈ 88% MVP Completion
```

---

# 21. Engineering Assessment

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
Role-Based Authorization
Staff Portal Architecture
Availability Scheduling Pattern
Protected Route Pattern
One-to-One User Mapping
Booking Lifecycle Management
```



---

# 22. Conclusion

The Beauty Salon Management System has evolved from a simple appointment booking application into a structured salon management platform.

The current implementation supports customer authentication, service catalog management, staff-service assignment, appointment booking, booking history, and scalable database architecture.

The project is prepared for future expansion into advanced scheduling, conflict prevention, notifications, billing, analytics, REST APIs, React frontend integration, and mobile applications while maintaining a clean and maintainable Django architecture.
