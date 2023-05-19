from django.shortcuts import render, redirect
from django.conf import settings
from utils.custom_decorators import get_user_permissions, is_in_group
from cinema.models import Film, Showing
from .forms import IndexForm
from datetime import datetime
from django.utils import timezone
import requests

# Create your views here


def index_view(request):
    perms = get_user_permissions(request)
    films = Film.objects.filter(archived=False)

    # get the date input from the form or use None as default
    date = None
    if request.method == "POST":
        form = IndexForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]

    # get all showings that start after the current time
    current_time = timezone.now()
    showings = Showing.objects.filter(start_time__gte=current_time, archived=False)

    # filter showings by date if provided
    if date is not None:
        showings = showings.filter(start_time__date=date, archived=False)

    # group showings by film
    showings_by_film = {}
    for showing in showings:
        film = showing.film
        if film not in showings_by_film:
            showings_by_film[film] = []
        showings_by_film[film].append(showing)

    # get poster for each film
    for film in films:
        title = film.title.replace(" ", "+")
        url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={title}"

        response = requests.get(url)
        data = response.json()

        if "Poster" in data:
            print("poster available")
            film.poster_url = data["Poster"]
            film.save()
        else:
            film.poster_url = ""
    print("USER PK:")
    print(request.user.pk)
    return render(
        request,
        "utils/index.html",
        {
            "user": request.user,
            "perms": perms,
            "films": films,
            "showings": showings,
            "showings_by_film": showings_by_film,
        },
    )


def view_my_details(request):
    """
    Handle a request for the user to see their details

    Returns:
        the users information page
    """
    perms = get_user_permissions(request)

    if perms == "-1":
        return redirect("login")

    if request.method == "GET":
        # Get the current logged-in user
        user = request.user
        # Render the template with the user's details
        return render(
            request, "utils/view_details.html", {"user": user, "perms": perms}
        )
