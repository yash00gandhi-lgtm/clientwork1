from django.urls import path
from .views import (
    dashboard_stats,
    dashboard_analytics,
    generate_report,
    
    dashboard_page,recent_payments
)

urlpatterns = [
    # 🔥 HOME (ROOT FIX)
    

    # 🔥 DASHBOARD PAGE
    path('dashboard/', dashboard_page),
    path('recent-payments/', recent_payments),

    # 🔥 APIs
    path('dashboard-stats/', dashboard_stats),
    path('dashboard-analytics/', dashboard_analytics),
    path('report/', generate_report),
]