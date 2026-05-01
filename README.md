# 🏋️ Axclusive Fitness CRM

### Build Strength. Automate Growth. Scale Your Gym.

A powerful, modern **Gym Management & Lead Automation System** built with Django — designed for real-world fitness businesses that want to **capture leads, automate workflows, and increase conversions**.

---

## 🚀 Live Vision

This system is built not just as a project, but as a **scalable SaaS-ready product** for gyms, trainers, and fitness brands.

---

## ✨ Features

### 🔥 Lead Management

* Capture leads from website forms
* Track lead status (New / Contacted / Converted)
* Organized dashboard for easy follow-up

### 📅 Booking System

* Seamless user booking flow
* Track user enrollments
* Structured data for business insights

### 🤖 Automation Engine

* Automatic email notifications
* Admin alerts on new leads
* Scalable notification logic

### 📊 Admin Dashboard

* Centralized control panel
* Monitor leads, bookings, and activity
* Clean UI with actionable data

### 💳 Payment Integration

* Integrated with Razorpay
* Smooth checkout experience
* Ready for real-world transactions

---

## 🧠 Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** SQLite (Dev) → PostgreSQL (Production Ready)
* **Frontend:** Django Templates (Custom UI)
* **Deployment:** Render (Cloud Ready)
* **Automation:** SMTP Email + Custom Logic

---

## ⚙️ Installation (Local Setup)

```bash
git clone https://github.com/yash00gandhi-lgtm/clientwork1.git
cd clientwork1

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file in root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

RAZORPAY_KEY_ID=your-key
RAZORPAY_KEY_SECRET=your-secret
```

---

## ▶️ Run Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🌍 Deployment

This project is fully **production-ready** and can be deployed on:

* Render (recommended)
* Any cloud supporting Django + PostgreSQL

---

## 💼 Business Use Case

This system is designed to:

* Help gyms **capture and convert leads**
* Automate repetitive tasks
* Provide a **professional digital presence**
* Scale into a full SaaS product

---

## 🧑‍💻 Author

**Yash Gandhi**
Building fitness-tech products & scalable systems.

---

## ⚡ Final Note

This is not just a CRUD app.
It’s a **foundation for a real fitness business system**.

If you’re serious about building something impactful — this is just the beginning.
