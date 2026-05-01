from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# =========================
# CLIENT SIDE (LOGIN REQUIRED)
# =========================

@login_required
def dashboard_page(request):
    return render(request, "client/dashboard.html")


@login_required
def leads_page(request):
    return render(request, "client/leads.html")


@login_required
def bookings_page(request):
    return render(request, "client/bookings.html")


@login_required
def automation_page(request):
    return render(request, "client/automation.html")


@login_required
def analytics_page(request):
    return render(request, "client/analytics.html")


# =========================
# PUBLIC SIDE (NO LOGIN)
# =========================

def landing_page(request):
    return render(request, "public/index.html")


def contact_page(request):
    return render(request, "public/contact.html")

def join(request):
    return render(request, 'join.html')


def booking_page(request):
    return render(request, "public/booking.html")