from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, create_payment
from . import views

router = DefaultRouter()
router.register('leads', LeadViewSet, basename='leads')

urlpatterns = [
    # 🔥 HTML PAGES
    path("pricing/", views.pricing_page),
    path("payment-success/", views.payment_success),
    path("payment-failed/", views.payment_failed),
    path("invoice/", views.invoice_page),

    # 🔥 PAYMENT API
    path("create-payment/", create_payment, name="create_payment"),
    path("verify-payment/", views.verify_payment),
]

# 🔥 DRF ROUTES ADD KAR
urlpatterns += router.urls