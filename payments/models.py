from django.db import models

from users.models import User

class transactionsModel(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    ]

    TRANSACTION_STATUSES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUSES)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payer_id = models.CharField(max_length=100, null=True, blank=True)
    approval_url = models.URLField(max_length=200, null=True, blank=True)
