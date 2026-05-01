from django.urls import path
from .views import auth_page, login_page

urlpatterns = [
    path('auth/', auth_page),     # API login
    path('login/', login_page),   # HTML page
]