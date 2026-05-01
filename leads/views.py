from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django.db import transaction
from datetime import date, time

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import razorpay
import json

from bookings.models import Booking
from .models import Lead, Payment
from .serializers import LeadSerializer
from automation.utils import send_lead_notification


# ========================
# 🌐 PAGES
# ========================

def pricing_page(request):
    return render(request, "pricing.html")

def payment_success(request):
    return render(request, "payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")

def invoice_page(request):
    return render(request, "invoice.html")


# ========================
# 🚀 LEAD VIEWSET
# ========================

class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = []

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['created_at']

    # 🔥 CREATE LEAD
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            lead = serializer.save()

            # 🔥 EMAIL AUTOMATION SAFE
            try:
                send_lead_notification(lead)
            except Exception as e:
                print("EMAIL ERROR:", e)

            return Response({
                "status": "success",
                "message": "Lead created successfully"
            }, status=201)

        except Exception as e:
            print("LEAD ERROR:", str(e))
            return Response({
                "error": str(e)
            }, status=500)

    # 📄 LIST
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })

    # 🔍 RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())

        return Response({
            "status": "success",
            "data": serializer.data
        })

    # ✏️ UPDATE
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "status": "success",
            "message": "Lead updated successfully",
            "data": serializer.data
        })

    # 🗑 DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "status": "success",
            "message": "Lead deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

    # 🎯 CONVERT → BOOKING
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        lead = self.get_object()

        if lead.status == "converted":
            return Response({
                "status": "error",
                "message": "Already converted"
            }, status=400)

        with transaction.atomic():
            lead.status = "converted"
            lead.save()

            booking = Booking.objects.create(
                name=lead.name,
                lead=lead,
                phone=lead.phone,
                program=lead.program or "General",
                trainer="Auto Assigned",
                date=date.today(),
                time=time(10, 0),
                status="confirmed"
            )

        return Response({
            "status": "success",
            "message": "Converted to booking",
            "booking_id": booking.id
        }, status=201)


# ========================
# 💳 PAYMENT CREATE
# ========================

@csrf_exempt
def create_payment(request):
    # ✅ Only POST allowed
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        # ✅ Safe JSON parse
        try:
            data = json.loads(request.body or "{}")
        except Exception:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # ✅ Env check
        key_id = getattr(settings, "RAZORPAY_KEY_ID", None)
        key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", None)

        if not key_id or not key_secret:
            return JsonResponse({"error": "Razorpay key missing"}, status=500)

        # ✅ Amount validation (in paise)
        amount = data.get("amount", 50000)
        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError()
        except Exception:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        customer_name = (data.get("customer_name") or "Guest").strip()

        # ✅ Razorpay client
        client = razorpay.Client(auth=(key_id, key_secret))

        # ✅ Create order
        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        # ✅ Save in DB
        Payment.objects.create(
            amount=amount,
            order_id=order["id"],
            customer_name=customer_name
        )

        # ✅ Response for frontend
        return JsonResponse({
            "key": key_id,
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR"
        })

    except Exception as e:
        print("PAYMENT ERROR:", str(e))  # logs me dikhega
        return JsonResponse({"error": "Server error"}, status=500)


# ========================
# ✅ PAYMENT VERIFY
# ========================

@csrf_exempt
def verify_payment(request):
    try:
        data = json.loads(request.body)

        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        customer_name = data.get("customer_name")

        payment = Payment.objects.get(order_id=order_id)

        payment.payment_id = payment_id
        payment.status = "paid"
        payment.customer_name = customer_name or "Customer"
        payment.save()

        Booking.objects.create(
            name=payment.customer_name,
            plan="Gym Membership",
            status="confirmed"
        )

        return JsonResponse({"status": "success"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)