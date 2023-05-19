from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ScreenForm, ShowingForm, FilmForm, CinemaForm, TicketForm
from .models import Screen, Cinema, Film, Showing, Ticket
from accounts.models import StudentDiscountRequest
from booking.models import Cancelation, Reservation
from authentication.models import User
from utils.custom_decorators import get_user_permissions, is_in_group
from datetime import datetime
from datetime import timedelta

# Create your views here.


def create_cinema(request):
    """
    Handle a user creating a cinema.

    If the request method is "POST", the function prompts the user to enter cinema information
    before being redirected to the cinema management page if succesful.
    If the request method is not "POST", the cinema form is displayed.

    Returns:
        If the request method is "POST" and the form is not valid:
            The cinema form, with the error message passed in as context.
        If the request method is not "POST":
            The cinema form form.
        Otherwise:
            A redirect to the cinema management page.
    """
    perms = get_user_permissions(request)
    if is_in_group(request.user, "admin"):
        if request.method == "POST":
            form = CinemaForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return redirect("manage_screens")
            else:
                form = CinemaForm()
                context = {"form": form, "user": request.user, "perms": perms}
                return render(request, "cinema/create_cinema.html", context)

        form = CinemaForm()
        context = {"form": form, "user": request.user, "perms": perms}
        return render(request, "cinema/create_cinema.html", context)
    else:
        return redirect("/no_access")


def screen_list(request):
    """
    Handle a screen management page request.

    This gets all screen and accompanying model data from the database to pass to the html template.

    Returns:
        screen management page with accompanying data
    """
    perms = get_user_permissions(request)
    print(perms)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    screens = Screen.objects.all()
    showings = Showing.objects.filter(archived=False).order_by("start_time")
    cinemas = Cinema.objects.all()
    context = {
        "user": request.user,
        "screens": screens,
        "showings": showings,
        "cinemas": cinemas,
        "perms": perms,
    }
    return render(request, "cinema/manage_screens.html", context)


def screen_create(request):
    """
    Handle a request to create a new screen.

    If the request method is "POST", the function prompts the user to enter screen information
    before being redirected to the screen management page if succesful.
    If the request method is not "POST", the screen form is displayed.

    Returns:
        If the request method is "POST" and the form is not valid:
            The screen form, with the error message passed in as context.
        If the request method is not "POST":
            The screen form form.
        Otherwise:
            A redirect to the screen management page.
    """
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    if request.method == "POST":
        form = ScreenForm(request.POST)
        if form.is_valid():
            screen = form.save()
            return redirect("manage_screens")

        elif not form.is_valid():
            context = {
                "form": form,
                "user": request.user,
                "screen": screen,
                "perms": perms,
                "form_errors": form.errors,
            }
            return render(request, "cinema/update_screen.html", context)

    form = ScreenForm()
    context = {
        "form": form,
        "user": request.user,
        "cinemas": Cinema.objects.all(),
        "perms": perms,
    }
    return render(request, "cinema/create_screen.html", context=context)


def screen_update(request, pk):
    """
    Handle a user requesting to update a screen

    Returns:
        If the form is invalid:
            screen form
        otherwise:
            redirect to screen management
    """
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    screen = get_object_or_404(Screen, pk=pk)
    if request.method == "POST":
        form = ScreenForm(request.POST, instance=screen)
        if form.is_valid():
            screen = form.save()
            return redirect("manage_screens")

        elif not form.is_valid():
            context = {
                "form": form,
                "user": request.user,
                "screen": screen,
                "perms": perms,
                "form_errors": form.errors,
            }
            return render(request, "cinema/update_screen.html", context)

    form = ScreenForm(instance=screen)
    context = {"form": form, "user": request.user, "screen": screen, "perms": perms}
    return render(request, "cinema/update_screen.html", context)


def screen_delete(request, pk):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    screen = get_object_or_404(Screen, pk=pk)
    screen.delete()
    return redirect("manage_screens")


def showings_list(request):
    """
    Handle a screen management page request.

    This gets all screen and accompanying model data from the database to pass to the html template.

    Returns:
        screen management page with accompanying data
    """
    perms = get_user_permissions(request)
    print(perms)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    showings = Showing.objects.filter(archived=False).order_by("start_time")
    archived_showings = Showing.objects.filter(archived=True).order_by("start_time")
    context = {
        "showings": showings,
        "perms": perms,
        "archived_showings": archived_showings,
    }
    return render(request, "cinema/showings_management.html", context)


def showing_create(request):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    films = Film.objects.filter(archived=False)
    screens = Screen.objects.all()

    if request.method == "POST":
        form = ShowingForm(request.POST)
        screen = Screen.objects.get(id=int(form.data.get("screen")))

        if form.data.get("start_time") < datetime.now().strftime("%Y-%m-%dT%H:%M"):
            form.errors["start_time"] = ["Start time must be in the future"]

        print(form.errors)
        if form.is_valid():
            f = form.save(commit=False)
            if not f.social_distancing:
                f.available_seats = screen.seating_capacity
                f.save()
            else:
                f.covid_capacity = screen.seating_capacity / 2
                f.available_seats = f.covid_capacity
                f.save()
            return redirect("manage_screens")
        else:
            print("invalid form")
    form = ShowingForm()
    context = {
        "form": form,
        "user": request.user,
        "films": films,
        "screens": screens,
        "perms": perms,
    }
    return render(request, "cinema/create_showing.html", context)


def films_list(request):
    """
    Handle a screen management page request.

    This gets all screen and accompanying model data from the database to pass to the html template.

    Returns:
        screen management page with accompanying data
    """
    perms = get_user_permissions(request)
    print(perms)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    films = Film.objects.filter(archived=False).order_by("title")
    archived_films = Film.objects.filter(archived=True).order_by("title")
    context = {"films": films, "perms": perms, "archived_films": archived_films}
    return render(request, "cinema/films_management.html", context)


def film_create(request, pk=None):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    if request.method == "POST":
        form = FilmForm(request.POST)
        if form.is_valid():
            f = form.save()
            f.length = timedelta(minutes=int(form.data.get("length")))
            f.save()
            return redirect("manage_screens")

    form = FilmForm()
    context = {"form": form, "user": request.user, "pk": pk, "perms": perms}
    return render(request, "cinema/create_film.html", context)


def film_delete(request, pk):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    film = get_object_or_404(Film, pk=pk)
    showings = Showing.objects.filter(film=film, archived=False)
    print(f"showings {showings}")
    if showings.exists():
        messages.error(
            request,
            "This film cannot be deleted because there are showings associated with it.",
        )
        return redirect("film_management")
    else:
        film.arhive()
        return redirect("film_management")


def users_list(request):
    """
    Handle a user management page request.

    This gets all users and accompanying model data from the database to pass to the html template.

    Returns:
        screen management page with accompanying data
    """
    perms = get_user_permissions(request)
    print(perms)
    if perms == "0" or perms == "1":
        return redirect("no_access")

    discount_requests = StudentDiscountRequest.objects.filter(approved=False)
    print(discount_requests)
    context = {
        "users": User.objects.all(),
        "discount_requests": discount_requests,
        "user": request.user,
        "perms": perms,
    }
    return render(request, "cinema/user_management.html", context)

    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    context = {
        "users": User.objects.filter(is_rep=False),
        "user": request.user,
        "perms": perms,
    }
    return render(request, "cinema/user_management.html", context)


def enable_user(request, pk):
    """
    Handle a user activating a user account via the user management page.

    Returns:
        A redirect to the user management page.
    """

    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    return redirect("user_management")


def disable_user(request, pk):
    """
    Handle a user disabling a user account via the user management page.

    Returns:
        A redirect to the user management page.
    """
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()
    return redirect("user_management")


def bookings_list(request):
    """
    Handle a booking management page request.

    This gets all bookings and accompanying model data from the database to pass to the html template.

    Returns:
        screen management page with accompanying data
    """
    perms = get_user_permissions(request)
    print(perms)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    context = {"cancellations": Cancelation.objects.all(), "perms": perms}
    return render(request, "cinema/manage_cancellations.html", context)


def approve_cancellation(request, pk):
    """
    Handle a cinema manager approving a user cancellation via the cancellation management page.

    Returns:
        A redirect to the cancellation management page.
    """
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    cancellation = get_object_or_404(Cancelation, pk=pk)
    cancellation.approved = True
    cancellation.save()

    booking = get_object_or_404(Reservation, pk=cancellation.reservation.pk)
    booking.cancelled = True
    booking.save()

    booking.reservee.account.balance = (
        float(booking.reservee.account.balance) + booking.booking_cost
    )
    booking.reservee.account.save()

    return redirect("cancellation_management")


def disapprove_cancellation(request, pk):
    """
    Handle a cinema manager disapproving a user cancellation via the cancellation management page.

    Returns:
        A redirect to the cancellation management page.
    """
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    cancellation = get_object_or_404(Cancelation, pk=pk)
    cancellation.approved = False
    cancellation.save()

    booking = get_object_or_404(Reservation, pk=cancellation.reservation.pk)
    booking.cancelled = False
    booking.save()

    return redirect("cancellation_management")


def delete_showing(request, pk):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    showing = get_object_or_404(Showing, pk=pk)

    # Need to check for related bookings, and decide what to do here. Maybe stripe has a refund?

    showing.archive()
    return redirect("showings_management")


def update_showing(request, pk):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    if request.method == "POST":
        form = ShowingForm(request.POST)
        if form.is_valid():
            # If the screen has changed, need to check if there are enough seats in the new screen.
            # If the film has changed, may need to update tickets?
            # If the start time has changed, need to check for conflict with other showings

            #    form.save()
            return redirect("manage_screens")

    showing = get_object_or_404(Showing, pk=pk)
    form = ShowingForm(instance=showing)
    context = {"form": form, "showing": showing, "perms": perms}
    return render(request, "cinema/update_showing.html", context)


def update_film(request, pk):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    film = get_object_or_404(Film, pk=pk)

    if request.method == "POST":
        form = FilmForm(request.POST)
        if form.is_valid():
            film.title = form.cleaned_data["title"]
            film.length = form.cleaned_data["length"]
            film.rating = form.cleaned_data["rating"]
            film.description = form.cleaned_data["description"]
            film.save()
            return redirect("manage_screens")

    form = FilmForm(instance=film)

    # Need to see how to default fill length and rating

    context = {"form": form, "film": film, "perms": perms}
    return render(request, "cinema/update_film.html", context)


def tickets_list(request):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    context = {"tickets": Ticket.objects.all(), "user": request.user, "perms": perms}
    return render(request, "cinema/tickets_management.html", context)


def update_ticket(request, pk):
    perms = get_user_permissions(request)
    if not perms == "3" and not perms == "4":
        return redirect("no_access")

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket.ticket_type = form.cleaned_data["ticket_type"]
            ticket.price = form.cleaned_data["price"]
            ticket.save()
            return redirect("ticket_management")

    form = TicketForm(instance=ticket)
    context = {"form": form, "ticket": ticket, "perms": perms}
    return render(request, "cinema/update_ticket.html", context)
