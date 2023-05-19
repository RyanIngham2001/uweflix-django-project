from django.shortcuts import render, redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from .serialisers import StripeInformationSerializer, GuestStripeInformationSerializer
import datetime
# Create your views here.

class StripePaymentView(APIView):
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Extract the payment amount and payment method ID from the request
        amount = request.data.get('amount')
        payment_method_id = request.data.get('payment_method_id')

        try:
            # Create a PaymentIntent with the specified amount and payment method ID
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True
            )

            # Return the client secret of the PaymentIntent to the frontend
            return Response({'client_secret': payment_intent.client_secret})

        except stripe.error.CardError as e:
            # If the payment is declined, return an error message
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GuestCheckoutSessionView(APIView):
    def post(self, request):
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        data=request.data

        is_many = data.get('is_many', False)
        serializer_data = data['serializer_data']
        
        serializer = GuestStripeInformationSerializer(data=serializer_data, many = is_many)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        line_items = []

        if is_many == True:
            for item in serializer.data:
                line_items.append(
                    {
                        'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                        'name': item['name'],
                        'description': item['description'],
                        },
                        'unit_amount': item['unit_amount'],
                        },
                    'quantity': item['quantity'],
                    }
                )
        else:
            line_items.append(
                    {
                        'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                        'name': serializer.data['name'],
                        'description': serializer.data['description'],
                        },
                        'unit_amount': serializer.data['unit_amount'],
                        },
                    'quantity': serializer.data['quantity'],
                    }
                )

        try:
            checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url=domain_url + 'paymentConfirm?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url,
            payment_method_types=['card'],
            mode='payment',
            line_items = line_items
            )

            return Response({'session_id': checkout_session.id, 'url': checkout_session.url}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class TopUpCheckoutSessionView(APIView):
    def post(self, request):
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        serializer = StripeInformationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        customerID = serializer.data['customerID']
        
        # If a Stripe API customer does not exist for the customer, create one
        if (customerID == "TBD"):

            newCustomer = stripe.Customer.create()
            customerID = str(newCustomer.id)

        line_items = []
        line_items.append(
            {
                'price_data': {
                'currency': 'gbp',
                'product_data': {
                'name': serializer.data['name'],
                'description': serializer.data['description'],
                },
                'unit_amount': serializer.data['unit_amount'],
                },
                'quantity': serializer.data['quantity'],
            }
        )

        try:
            checkout_session = stripe.checkout.Session.create(
            success_url=domain_url,
            cancel_url=domain_url,
            payment_method_types=['card'],
            mode='payment',
            line_items = line_items,
            customer = customerID,

            )

            return Response({
                'session_id': checkout_session.id,
                'url': checkout_session.url,
                'customerID' : customerID},
                status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TopUpHistory(APIView):
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        payment_intents = []

        config = int(request.data['config'])
        customer_id = request.data['customer_id']
        today = datetime.date.today()

        if (config == 1):
            first_day_of_this_month = datetime.date(today.year, today.month, 1)
            last_day_of_previous_month = first_day_of_this_month - datetime.timedelta(days=1)
            last_day_of_previous_month_dt = datetime.datetime.combine(last_day_of_previous_month, datetime.datetime.min.time())

            payment_intents = stripe.PaymentIntent.list(
                limit=100,
                created={
                    'gte': int(last_day_of_previous_month_dt.timestamp()),
                },
                customer=customer_id
            )
        
        elif (config == 2):
            last_month_start = datetime.datetime(today.year, today.month-1, 1)
            last_month_end = datetime.datetime(today.year, today.month, 1) - datetime.timedelta(days=1)

            payment_intents = stripe.PaymentIntent.list(
                limit=100,
                created={
                    'gte': int(datetime.datetime.timestamp(last_month_start)),

                    # One day added in seconds to include end date in list
                    'lt': int(datetime.datetime.timestamp(last_month_end)) + 86400
                },
                customer=customer_id
            )

        return Response({
                'payment_history' : payment_intents},
                status=status.HTTP_201_CREATED) 
        