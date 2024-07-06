# payment_gateway/views.py
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.helpers import Authentication
from .models import transactionsModel
from .serializer import TransactionSerializer
import requests
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models import User

class initiatePaymentView(APIView):
    authentication_classes = [Authentication]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "amount":openapi.Schema(type=openapi.TYPE_STRING),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'transaction_type': openapi.Schema(type=openapi.TYPE_STRING),
        }))
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'USD')
        return_url = 'http://127.0.0.1:8000/payment/success'
        cancel_url = 'http://127.0.0.1:8000/payment/cancel'
        transaction_type = request.data.get('transaction_type')

        status, payment_id, approval_url = self.make_paypal_payment(amount, currency, return_url, cancel_url)

        if not status:
            return Response({'error': payment_id}, status=status.HTTP_400_BAD_REQUEST)
        user=get_object_or_404(User,user=request.user)
        transaction = transactionsModel.objects.create(
            user=user,
            amount=amount,
            status='Pending',
            transaction_type=transaction_type,
            payment_id=payment_id,
            approval_url=approval_url
        )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=201)

    def make_paypal_payment(self, amount, currency, return_url, cancel_url):
        client_id = "AbizyV7qfPHdg6jambSqiUVrfMKIkGPnbKk90cQFbtIpzZP6VBl6B1yQquionrnXp_J7zojaioNv3WYm"
        secret = "EGGsnJRT7c9Zr7ZyVKkO3yOKUQ86lGeJj4eef6XioRMM1C0tjbD6hLMnkDcm79_azduM3a4f52fc8D3s"
        url = "https://api.sandbox.paypal.com"

        base_url = url
        token_url = base_url + '/v1/oauth2/token'
        payment_url = base_url + '/v1/payments/payment'

        token_payload = {'grant_type': 'client_credentials'}
        token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

        if token_response.status_code != 200:
            return False, "Failed to authenticate with PayPal API", None

        access_token = token_response.json()['access_token']

        payment_payload = {
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {'total': str(amount), 'currency': currency},
                'description': 'Transaction description'
            }],
            'redirect_urls': {
                'return_url': return_url,
                'cancel_url': cancel_url
            }
        }

        payment_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payment_response = requests.post(payment_url, data=json.dumps(payment_payload), headers=payment_headers)

        if payment_response.status_code != 201:
            return False, 'Failed to create PayPal payment.', None

        payment_id = payment_response.json()['id']
        approval_url = next(link['href'] for link in payment_response.json()['links'] if link['rel'] == 'approval_url')

        return True, payment_id, approval_url

class PaymentVerifyView(APIView):
    def get(self, request):
        payment_id = request.query_params.get('paymentId')
        payer_id = request.query_params.get('PayerID')

        if not payment_id or not payer_id:
            return Response({'error': 'Invalid payment_id or payer_id'}, status=status.HTTP_400_BAD_REQUEST)

        transaction = get_object_or_404(transactionsModel, payment_id=payment_id)

        status = self.execute(payment_id, payer_id)
        print(status)
        if status:
            transaction.status = 'Completed'
            transaction.payer_id = payer_id
            transaction.save()
            return Response({'status': 'Payment completed successfully'}, status=200)
        else:
            transaction.status = 'Failed'
            transaction.save()
            return Response({'status': 'Payment failed'}, status=400)

    def execute(self, payment_id, payer_id):
        client_id = "AbizyV7qfPHdg6jambSqiUVrfMKIkGPnbKk90cQFbtIpzZP6VBl6B1yQquionrnXp_J7zojaioNv3WYm"
        secret = "EGGsnJRT7c9Zr7ZyVKkO3yOKUQ86lGeJj4eef6XioRMM1C0tjbD6hLMnkDcm79_azduM3a4f52fc8D3s"
        url = "https://api.sandbox.paypal.com"

        # Set up API endpoints
        base_url = url
        token_url = base_url + '/v1/oauth2/token'

        # Request an access token
        token_payload = {'grant_type': 'client_credentials'}
        token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

        if token_response.status_code != 200:
            raise Exception('Failed to authenticate with PayPal API.')

        access_token = token_response.json()['access_token']

        # Retrieve payment details
        payment_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        data = {"payer_id":payer_id}

        response = requests.post(f'https://api-m.sandbox.paypal.com/v1/payments/payment/{payment_id}/execute', headers=payment_headers, data=json.dumps(data))

        return response.json()

class userTransactionHistoryView(APIView):
    authentication_classes = [Authentication]
    def get(self, request):
        user=get_object_or_404(User,user=request.user)
        transactions = transactionsModel.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

    
class cancelView(APIView):
    def get(self, request):
        payment_id = request.query_params.get('paymentId')
        payer_id = request.query_params.get('PayerID')

        if not payment_id or not payer_id:
            return Response({'error': 'Invalid payment_id or payer_id'}, status=status.HTTP_400_BAD_REQUEST)

        transaction = get_object_or_404(transactionsModel, payment_id=payment_id)
       
        if transaction:
            transaction.status = 'Cancelled'
            transaction.payer_id = payer_id
            transaction.save()
            return Response({'status': 'Payment Cancelled'}, status=200)
        else:
            
            return Response({'status': 'Something Went Wrong'}, status=400)



class WithdrawalRequestView(APIView):
    authentication_classes = [Authentication]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "amount":openapi.Schema(type=openapi.TYPE_STRING),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            "recipient_email": openapi.Schema(type=openapi.TYPE_STRING)
        }))
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'USD')
        recipient_email = request.data.get('recipient_email')

        status, payout_batch_id = self.make_paypal_payout(amount, currency, recipient_email)

        if not status:
            return Response({'error': 'Failed to process withdrawal'}, status=400)

        
        user=User.objects.get(id=1)
        transaction = transactionsModel.objects.create(
            user=user,
            amount=amount,
            status='Pending',
            transaction_type='Withdrawal',
            payment_id=payout_batch_id,
        )

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=201)

    def make_paypal_payout(self, amount, currency, recipient_email):
        client_id = "AbizyV7qfPHdg6jambSqiUVrfMKIkGPnbKk90cQFbtIpzZP6VBl6B1yQquionrnXp_J7zojaioNv3WYm"
        secret = "EGGsnJRT7c9Zr7ZyVKkO3yOKUQ86lGeJj4eef6XioRMM1C0tjbD6hLMnkDcm79_azduM3a4f52fc8D3s"
        url = "https://api.sandbox.paypal.com"

        base_url = url
        token_url = base_url + '/v1/oauth2/token'
        payout_url = base_url + '/v1/payments/payouts'

        token_payload = {'grant_type': 'client_credentials'}
        token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

        if token_response.status_code != 200:
            return False, "Failed to authenticate with PayPal API"

        access_token = token_response.json()['access_token']

        payout_payload = {
            "sender_batch_header": {
                "sender_batch_id": str(uuid.uuid4()),
                "email_subject": "You have a payout!",
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": str(amount),
                        "currency": currency
                    },
                    "receiver": recipient_email,
                    "note": "Thank you for using our service!"
                }
            ]
        }

        payout_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        payout_response = requests.post(payout_url, data=json.dumps(payout_payload), headers=payout_headers)
        if payout_response.status_code != 201:
            return False, 'Failed to create PayPal payout.'

        payout_batch_id = payout_response.json()['batch_header']['payout_batch_id']
        return True, payout_batch_id