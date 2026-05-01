from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django.db import transaction
from datetime import date, time

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from bookings.models import Booking
from .models import Lead
from .serializers import LeadSerializer
from .models import Payment
from automation.utils import send_lead_notification
from bookings.models import Booking
from leads.models import Lead

from django.shortcuts import render

def pricing_page(request):
    return render(request, "pricing.html")

def payment_success(request):
    return render(request, "payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")

def invoice_page(request):
    return render(request, "invoice.html")


class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = []

    # 🔍 FILTER / SEARCH / ORDER
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['created_at']

    # 🚀 CREATE (AUTOMATION TRIGGER)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
                    lead = serializer.save()
        print("✅ LEAD CREATED:", lead.email)

        # 🔥 AUTOMATION (DEBUG)
        try:
            print("🚀 CALLING AUTOMATION...")
            send_lead_notification(lead)
            print("✅ AUTOMATION DONE")
        except Exception as e:
            print("❌ AUTOMATION ERROR:", str(e))

            # 🔥 AUTOMATION (safe)
            try:
                send_lead_notification(lead)
            except Exception as e:
                print("❌ AUTOMATION ERROR:", str(e))

        return Response({
            "status": "success",
            "message": "Lead created successfully 🚀",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

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

    # 🎯 CONVERT LEAD → BOOKING
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        lead = self.get_object()

        if lead.status == "converted":
            return Response({
                "status": "error",
                "message": "Lead already converted"
            }, status=status.HTTP_400_BAD_REQUEST)

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
            "message": "Lead converted to booking 🎯",
            "booking_id": booking.id
        }, status=status.HTTP_201_CREATED)
    
import razorpay
from django.conf import settings

from django.http import JsonResponse

def create_payment(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    data = json.loads(request.body)
    customer_name = data.get("customer_name")
    amount = int(data.get("amount", 50000))

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # DB me save
    Payment.objects.create(
    user=request.user,
    amount=amount,
    order_id=order['id'],
    customer_name=data.get("customer_name")
)

    return JsonResponse({
        "order_id": order['id'],
        "key": settings.RAZORPAY_KEY_ID,
        "amount": amount
    })

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def verify_payment(request):
    import json
    data = json.loads(request.body)

    payment_id = data.get("razorpay_payment_id")
    order_id = data.get("razorpay_order_id")
    customer_name = data.get("customer_name")

    # ✅ FIRST GET PAYMENT
    payment = Payment.objects.get(order_id=order_id)

    # ✅ USER NAME FIX (optional)
    if not payment.user.name:
        payment.user.name = payment.user.username or payment.user.email.split("@")[0]
        payment.user.save()

    # ✅ SAVE PAYMENT DATA
    payment.payment_id = payment_id
    payment.status = "paid"
    payment.customer_name = customer_name or "Customer"
    payment.save()

    # ✅ BOOKING CREATE
    Booking.objects.create(
        user=payment.user,
        plan="Gym Membership",
        status="confirmed"
    )

    return JsonResponse({"status": "success"})