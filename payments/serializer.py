# payment_gateway/serializers.py
from rest_framework import serializers
from .models import transactionsModel

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactionsModel
        fields = '__all__'
