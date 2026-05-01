from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from leads.models import Lead
from bookings.models import Booking

from django.shortcuts import render



from django.contrib.auth.decorators import login_required

@login_required(login_url='/api/auth/')
def dashboard_page(request):
    return render(request, 'dashboard.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    total_leads = Lead.objects.count()
    total_bookings = Booking.objects.filter(status='confirmed').count()

    conversion_rate = 0
    if total_leads > 0:
        conversion_rate = (total_bookings / total_leads) * 100

    return Response({
        "total_leads": total_leads,
        "total_bookings": total_bookings,
        "conversion_rate": round(conversion_rate, 2)
    })


@api_view(['GET'])
def generate_report(request):
    total_leads = Lead.objects.count()
    total_bookings = Booking.objects.filter(status='confirmed').count()

    conversion_rate = 0
    if total_leads > 0:
        conversion_rate = (total_bookings / total_leads) * 100

    # 🔥 SMART LOGIC
    if conversion_rate >= 70:
        summary = "Excellent performance 🚀"
        suggestions = ["Scale ads", "Increase pricing"]
    elif conversion_rate >= 40:
        summary = "Good, but can improve ⚡"
        suggestions = ["Improve follow-ups", "Better closing"]
    else:
        summary = "Needs improvement ⚠️"
        suggestions = ["Call leads faster", "Train sales skills"]

    return Response({
        "summary": summary,
        "conversion_rate": round(conversion_rate, 2),
        "suggestions": suggestions
    })


from datetime import timedelta
from django.utils import timezone
from django.db.models import Count


@api_view(['GET'])
def dashboard_analytics(request):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=6)

    leads = Lead.objects.filter(created_at__date__gte=last_7_days)
    bookings = Booking.objects.filter(created_at__date__gte=last_7_days)

    total_leads = leads.count()
    total_bookings = bookings.count()

    conversion_rate = 0
    if total_leads > 0:
        conversion_rate = round((total_bookings / total_leads) * 100, 2)

    leads_by_date = leads.values('created_at__date').annotate(count=Count('id'))
    bookings_by_date = bookings.values('created_at__date').annotate(count=Count('id'))

    leads_dict = {str(item['created_at__date']): item['count'] for item in leads_by_date}
    bookings_dict = {str(item['created_at__date']): item['count'] for item in bookings_by_date}

    daily_data = []

    for i in range(7):
        day = last_7_days + timedelta(days=i)
        day_str = str(day)

        daily_data.append({
            "date": day_str,
            "leads": leads_dict.get(day_str, 0),
            "bookings": bookings_dict.get(day_str, 0),
        })

    return Response({
        "total_leads": total_leads,
        "total_bookings": total_bookings,
        "conversion_rate": conversion_rate,
        "daily_data": daily_data
    })

from leads.models import Payment

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_payments(request):
    payments = Payment.objects.filter(status="paid").order_by('-created_at')[:5]

    data = []
    for p in payments:
        data.append({
            "user": p.customer_name or "Customer",
            "amount": p.amount,
            "status": p.status,
            "date": p.created_at.strftime("%d %b")
        })

    return Response(data)