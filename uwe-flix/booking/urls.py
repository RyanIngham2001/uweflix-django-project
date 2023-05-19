
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('paymentConfirm/', views.payment_confirm, name='paymentConfirm'),
    path('make_booking/', views.make_booking, name="make_booking"),
    path('make_booking/<str:pk>', views.make_booking, name="make_specific_booking"),
    path('view_bookings/', views.view_bookings, name="view_bookings"),
    path('search_booking/', views.search_booking, name="search_booking"),
    path('request_cancelation/<str:pk>', views.request_cancelation, name="request_cancelation"),
]
