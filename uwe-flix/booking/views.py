from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from clubs.models import ClubRepresentative, Club
from accounts.models import Account
from .models import Reservation, Showing, Cancelation, Ticket, Film, StripeInformation
from .forms import ReservationForm, ReservationSearch
from .serializers import GuestStripeInformationSerializer
from utils.custom_decorators import get_user_permissions, is_in_group
import requests
from datetime import datetime
from django.conf import settings
from rest_framework import status


def payment_confirm(request):
    perms = get_user_permissions(request)

    session_id = request.GET.get("session_id")

    context = {"perms": perms, "session_id": session_id}
    return render(request, "paymentConfirm.html", context)


# View to create a booking
def make_booking(request, pk):
    user = request.user
    showing = Showing.objects.get(id=pk)
    perms = get_user_permissions(request)
    form = ReservationForm(user=request.user)
    form.fields["showing"].initial = Showing.objects.get(id=pk)

    # If the submit button is pressed
    if request.method == "POST":
        user = request.user

        # Create a temp form to get the selected showing
        form = ReservationForm(request.POST, user=user)
        form.fields["showing"].initial = Showing.objects.get(id=pk)
        print("here1")
        if form.is_valid():
            print("here2")
            reservation = form.save(commit=False)

            showing = get_object_or_404(Showing, pk=reservation.showing_id)
            film = get_object_or_404(Film, pk=showing.film_id)

            adultTicket = get_object_or_404(Ticket, pk=1)
            studentTicket = get_object_or_404(Ticket, pk=2)
            childTicket = get_object_or_404(Ticket, pk=3)

            # Calculate the cost of the order based on the ticket pricing in the ticket model
            student_cost = reservation.student_quantity * Decimal(studentTicket.price)
            child_cost = reservation.child_quantity * Decimal(childTicket.price)
            adult_cost = reservation.adult_quantity * Decimal(adultTicket.price)

            total_cost = student_cost + child_cost + adult_cost

            # Check if the user is logged in, if so, get the user/club discount rate
            if request.user.is_authenticated:
                discount = Decimal(1 - request.user.discount_rate)

                total_cost * discount

            # Create the final form with the reservee and cost added
            if request.user.is_authenticated:
                reservation.reservee = request.user
            else:
                reservation.reservee = None

            reservation.booking_cost = total_cost

            # If the form is all correct, save the booking, update the amount of tickets and redirect to checkout
            current_time = timezone.now().replace(second=0, microsecond=0)
            if showing.start_time >= current_time:
                total_seats = (
                    reservation.student_quantity
                    + reservation.adult_quantity
                    + reservation.child_quantity
                )

                # If not a logged in user, need to redirect to payment page for card details and order confirmation
                if not request.user.is_authenticated:
                    if int(showing.available_seats) >= total_seats:
                        order_items = []

                        # Creates the product data to be passed to the Stripe Payments app for checkout
                        if int(reservation.child_quantity) > 0:
                            order_items.append(
                                StripeInformation(
                                    "Child Ticket",
                                    (
                                        "Child ticket for the showing of "
                                        + film.title
                                        + " at "
                                        + str(showing.start_time)
                                    ),
                                    (int(childTicket.price * 100)),
                                    (int(reservation.child_quantity)),
                                )
                            )

                        if int(reservation.student_quantity) > 0:
                            order_items.append(
                                StripeInformation(
                                    "Student Ticket",
                                    (
                                        "Student ticket for the showing of "
                                        + film.title
                                        + " at "
                                        + str(showing.start_time)
                                    ),
                                    (int(studentTicket.price * 100)),
                                    (int(reservation.student_quantity)),
                                )
                            )

                        if int(reservation.adult_quantity) > 0:
                            order_items.append(
                                StripeInformation(
                                    "Adult Ticket",
                                    (
                                        "Adult ticket for the showing of "
                                        + film.title
                                        + " at "
                                        + str(showing.start_time)
                                    ),
                                    (int(adultTicket.price * 100)),
                                    (int(reservation.adult_quantity)),
                                )
                            )

                        if len(order_items) == 1:
                            serializer = GuestStripeInformationSerializer(
                                order_items[0]
                            )
                            data = {
                                "is_many": False,
                                "serializer_data": serializer.data,
                            }
                        elif len(order_items) > 1:
                            serializer = GuestStripeInformationSerializer(
                                order_items, many=True
                            )
                            data = {"is_many": True, "serializer_data": serializer.data}
                        elif len(order_items) < 1:
                            context = {
                                "form": form,
                                "perms": perms,
                                "error": True,
                                "error_message": "Please select a number of tickets.",
                            }
                            return render(request, 'make_booking.html', context)
                        
                        response = requests.post('http://stripe:8001/api/guest_create_checkout_session/', json=data)

                        response_dict = response.json()

                        if response.status_code == status.HTTP_201_CREATED:
                            #### Redirects to checkout above, then need to place booking upon success
                            # Save the booking
                            reservation.showing = showing
                            reservation.guest_reservee = response_dict["session_id"]
                            reservation.save()

                            # Update the available seats
                            showing.available_seats = (
                                int(showing.available_seats) - total_seats
                            )
                            showing.save()

                            return redirect(response_dict["url"])

                        else:
                            context = {
                                "form": form,
                            }
                            return render(request, "make_booking.html", context)

                if user.is_rep == True:
                    club_representative = get_object_or_404(
                        ClubRepresentative, linked_user=user
                    )
                    club = get_object_or_404(
                        Club, representative=club_representative.id
                    )
                    account = club.account

                else:
                    account = get_object_or_404(Account, pk=user.account_id)

                if account.balance >= total_cost:
                    if int(showing.available_seats) >= total_seats:
                        # Save the booking
                        reservation.showing = showing
                        reservation.save()

                        # Update the available seats
                        showing.available_seats = (
                            int(showing.available_seats) - total_seats
                        )
                        showing.save()

                        # Update account balance
                        account.balance = account.balance - total_cost
                        account.save()
                        return redirect("view_bookings")

                    else:
                        context = {
                            "form": form,
                            "perms": perms,
                            "showing": showing,
                            "user": user,
                            "error": True,
                            "error_message": "Invalid seats in showing for booking. Please select a different showing.",
                        }
                        return render(request, "make_booking.html", context)

                else:
                    context = {
                        "form": form,
                        "perms": perms,
                        "showing": showing,
                        "user": user,
                        "error": True,
                        "error_message": "Invalid funds for booking. Please top-up account.",
                    }
                    return render(request, "make_booking.html", context)

            else:
                context = {
                    "form": form,
                    "perms": perms,
                    "showing": showing,
                    "user": user,
                    "error": True,
                    "error_message": "The start time for that showing has elapsed. Please select a different showing.",
                }
                return render(request, "make_booking.html", context)

    context = {
        "form": form,
        "perms": perms,
        "showing": showing,
        "user": user,
    }

    return render(request, "make_booking.html", context)


# View to request a cancellation
def request_cancelation(request, pk):
    # Upon request, get relevent reservation and make a cancellation object assigned to the reservation
    reservation = Reservation.objects.get(id=pk)

    reservation.cancellation_requested = True
    reservation.save()

    cancelation = Cancelation(reservation=reservation)

    cancelation.save()

    return redirect("view_bookings")


# View for viewing all of the bookings relating to the account
def view_bookings(request):
    perms = get_user_permissions(request)
    try:
        # Get all bookings for the current user
        upcoming_bookings = Reservation.objects.filter(
            reservee=request.user, showing__start_time__gte=datetime.now()
        ).order_by("-showing__start_time")
        past_bookings = Reservation.objects.filter(
            reservee=request.user, showing__start_time__lte=datetime.now()
        ).order_by("-showing__start_time")
        cancelations = Cancelation.objects.all()
        context = {
            "upcoming_bookings": upcoming_bookings,
            "past_bookings": past_bookings,
            "cancelations": cancelations,
            "perms": perms,
        }
        return render(request, "view_bookings.html", context)
    # If an error occurs or if user isn't logged in, redirect to no access page
    except:
        return redirect("/no_access")


def search_booking(request):
    perms = get_user_permissions(request)

    if request.method == "POST":
        form = ReservationSearch(request.POST)

        if form.is_valid():
            try:
                upcoming_booking = Reservation.objects.get(
                    guest_reservee=request.POST.get("guest_reservee"),
                    showing__start_time__gte=datetime.now(),
                )
                context = {"config": 1, "up_book": upcoming_booking, "perms": perms}
                return render(request, "view_guest_booking.html", context)

            except:
                pass
            try:
                past_booking = Reservation.objects.get(
                    guest_reservee=request.POST.get("guest_reservee"),
                    showing__start_time__lte=datetime.now(),
                )
                context = {"config": 2, "past_book": past_booking, "perms": perms}
                return render(request, "view_guest_booking.html", context)

            except:
                pass

            context = {"config": 0, "perms": perms}
            return render(request, "view_guest_booking.html", context)
        else:
            print(form.errors)

    form = ReservationSearch()
    context = {"form": form, "perms": perms}

    return render(request, "search_booking.html", context)