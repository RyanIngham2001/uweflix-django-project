from django.urls import path

from . import views

app_name = 'stripePayments'

urlpatterns = [
    path('guest_create_checkout_session/', views.GuestCheckoutSessionView.as_view(), name='guest_create_checkout_session'),
    path('top_up_create_checkout_session/', views.TopUpCheckoutSessionView.as_view(), name='top_up_create_checkout_session'),
    path('top_up_history/', views.TopUpHistory.as_view(), name='top_up_history'),
]