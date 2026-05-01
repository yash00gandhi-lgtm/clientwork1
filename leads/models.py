from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)

    status = models.CharField(
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('converted', 'Converted')
        ],
        default='new',
        max_length=20
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.conf import settings
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()  # in paise
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, default="created")
    created_at = models.DateTimeField(auto_now_add=True)