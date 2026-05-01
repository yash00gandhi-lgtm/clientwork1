from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [

    # ===== CLIENT (ADMIN PANEL) =====
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('leads/', views.leads_page, name='leads'),
    path('bookings/', views.bookings_page, name='bookings'),
    path('automation/', views.automation_page, name='automation'),
    path('analytics/', views.analytics_page, name='analytics'),
    path('join/', views.join, name='join'),
    path("success/", TemplateView.as_view(template_name="success.html")),

    # ===== PUBLIC (CUSTOMER SIDE) =====
    path('', views.landing_page, name='index'),
    path('contact/', views.contact_page, name='contact'),
    path('book/', views.booking_page, name='booking'),
]