# E-RTO Service – Electronic Regional Transport Office

##  Project Overview

E-RTO Service is a web-based Electronic Regional Transport Office management system developed to digitalize and simplify various RTO-related services.

The application provides a centralized platform where users can register, verify their accounts, apply for driving licenses, register vehicles, submit complaints, provide feedback, and interact with a chatbot for basic assistance.

A dedicated administrator panel allows authorized administrators to monitor applications, approve or reject driving license and vehicle registration requests, manage complaints, review feedback, and monitor system activities through a dashboard.

---

##  Aim of the Project

The main aim of the E-RTO System is to provide a secure, efficient, user-friendly, and centralized digital platform for managing transport-related services while reducing paperwork, manual processing, waiting time, and administrative effort.

---

##  Key Features

### User Features

- User registration
- Mobile OTP verification
- Secure user login
- User dashboard
- Driving License application
- Document upload
- Application status tracking
- Vehicle registration
- Vehicle number format validation
- Complaint submission
- Feedback submission
- Interactive chatbot
- Logout functionality

###  Admin Features

- Separate admin login
- Secure admin authentication
- View all driving license applications
- Approve or reject driving license applications
- View vehicle registrations
- Approve or reject vehicle registrations
- View user complaints
- Manage application status
- View user feedback
- Dashboard statistics
- Real-time/auto-updating dashboard information

---

##  Vehicle Number Validation

The system validates vehicle registration numbers according to the following format:

AA 00 AA 0000

Example:

KA 01 AB 1234

Invalid formats are rejected by the system.

---

##  Admin Dashboard

The administrator dashboard provides information such as:

- Total applications
- Pending applications
- Approved applications
- Rejected applications
- Vehicle registrations
- Complaints
- Feedback

Charts and statistics are displayed to help administrators monitor the system efficiently.

---

##  Chatbot

The project includes an interactive chatbot that provides users with basic information and assistance related to E-RTO services.

The chatbot is designed to improve the user experience and provide quick responses to frequently asked questions.

---

##  Technologies Used

### Backend

- Python
- Flask

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap
- Chart.js

### Database

- SQLite
- SQL

### Python Libraries

- Flask
- sqlite3
- os
- re
- random
- json
- Werkzeug
- Jinja2
- Gunicorn

### Development Tools

- Visual Studio Code
- Git
- GitHub

### Deployment

- Render

---

##  System Architecture

The system follows a client-server architecture.

```text
                ┌───────────────────┐
                │       USER        │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │   E-RTO WEBSITE   │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │   FLASK BACKEND   │
                └─────────┬─────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       ┌──────────────┐       ┌──────────────┐
       │    SQLite    │       │     ADMIN    │
       │   Database   │       │    PANEL     │
       └──────────────┘       └──────────────┘
