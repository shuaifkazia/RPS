# payment_gateway/urls.py
from django.urls import path
from .views import initiatePaymentView, PaymentVerifyView, userTransactionHistoryView, WithdrawalRequestView, cancelView

urlpatterns = [

    path('initiate-/payment/', initiatePaymentView.as_view(), name='initiate_payment'),
    path('user-transaction_history/', userTransactionHistoryView.as_view(), name='user-transaction_history'),
    path('success/', PaymentVerifyView.as_view(), name='transaction-history'),
    path('cancel/', cancelView.as_view(), name='transaction-history'),
    # path('request_withdrawal/', WithdrawalRequestView.as_view(), name='request-withdrawal'),
]
