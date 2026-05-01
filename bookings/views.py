from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Booking
from .serializers import BookingSerializer

from automation.utils import send_booking_confirmation

from django.shortcuts import render




class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer
    permission_classes = []

    # 🔥 FILTER / SEARCH / ORDER
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'program']
    search_fields = ['name', 'phone']
    ordering_fields = ['created_at', 'date']

    # 🔥 CREATE (WITH AUTOMATION)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            booking = serializer.save()

            # 🚀 EMAIL CONFIRMATION
            try:
                send_booking_confirmation(booking)
            except Exception as e:
                print("❌ BOOKING EMAIL ERROR:", e)

        return Response({
            "status": "success",
            "message": "Booking created successfully 🎯",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    # 🔥 LIST (PAGINATION SAFE)
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

    # 🔥 RETRIEVE
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())

        return Response({
            "status": "success",
            "data": serializer.data
        })

    # 🔥 UPDATE
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "status": "success",
            "message": "Booking updated successfully",
            "data": serializer.data
        })

    # 🔥 DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "status": "success",
            "message": "Booking deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)