from django.contrib import admin

from .models import Lead, Payment

admin.site.register(Lead)
admin.site.register(Payment)
