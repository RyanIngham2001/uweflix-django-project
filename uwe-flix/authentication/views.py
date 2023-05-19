from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.db.utils import IntegrityError
from .forms import UserRegistrationForm, ElevateUserForm
from .models import User, Group
from clubs.models import ClubRepresentative
from accounts.models import UserAccount
from utils.custom_decorators import get_user_permissions
from utils.custom_decorators import is_in_group
from datetime import date
from datetime import datetime, timedelta

# Create your views here


def login_view(request):
    """
    Handle a user logging in to uweflix.

    If the request method is "POST", the function checks the provided username and password against the
    database to authenticate the user. If the user is authenticated, the user is logged in and redirected
    to the index page. If the user is not authenticated, an error message is displayed and the login form
    is shown again. If the request method is not "POST", the login form is displayed.

    Returns:
        If the request method is "POST" and the user is not authenticated:
            The login form, with the error message passed in as context.
        If the request method is not "POST":
            The login form.
        Otherwise:
            A redirect to the index page.
    """

    # If the user has submitted the form
    if request.method == "POST":
        # Validate the form data
        username = request.POST.get("inputUsername")
        password = request.POST.get("inputPassword")
        user = authenticate(request, username=username, password=password)

        # If the user is authenticated
        if user is not None:
            if not user.account:
                user_acc = UserAccount.objects.create(
                    discount_rate=5,
                    balance=0,
                    name=f"{user.username}_account",
                )
                user.account = user_acc
                user.save()

            # Check if the user is a member of cinema_manager_temp and their expiry date has passed
            try:
                cinema_manager_temp_group = Group.objects.get(
                    name="cinema_manager_temp"
                )
                if cinema_manager_temp_group in user.groups.all():
                    today = date.today()
                    expiry_date_str = (
                        user.groups.filter(name="cinema_manager_temp")
                        .first()
                        .temporarygroup.expiry_date
                    )
                    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                    if today > expiry_date:
                        user.groups.remove(cinema_manager_temp_group)
            except Group.DoesNotExist:
                pass

            login(request, user)
            return redirect("/index")

        # If the user is not authenticated
        else:
            messages.error(request, "invalid login credentials. Please try again.")
            return render(request, "authentication/login.html", {"error": True})

    # If the user has not submitted the form
    else:
        # Display the login form
        return render(request, "authentication/login.html")


def club_rep_login(request):
    if request.method == "POST":
        rep_id = request.POST.get("inputUsername")
        print(rep_id)
        password = request.POST.get("inputPassword")
        user = authenticate(request, username=rep_id, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid representative ID or password"
            print(error_message)
            club_reps = ClubRepresentative.objects.all()
            context = {"error": True, "club_reps": club_reps}
            return render(request, "authentication/club_rep_login.html", context)

    else:
        club_reps = ClubRepresentative.objects.all()
        print(club_reps)
        context = {"club_reps": club_reps}
        return render(request, "authentication/club_rep_login.html", context)


def logout_view(request):
    perms = get_user_permissions(request)

    if perms == "-1":
        return redirect("login")

    logout(request)
    return render(request, "authentication/login.html")


def register_view(request):
    """
    Handle a user registering for uweflix.

    If the request method is "POST", the function prompts the user to enter user information
    and password verification before being redirected to the index page if succesful.
    If the request method is not "POST", the login form is displayed.

    Returns:
        If the request method is "POST" and the form is not valid:
            The registration form, with the error message passed in as context.
        If the request method is not "POST":
            The registration form form.
        Otherwise:
            A redirect to the index page.
    """
    perms = get_user_permissions(request)
    print(perms)
    if not perms == "-1":
        print("ERROR")
        return redirect("no_access")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            user_account = UserAccount.objects.create(
                discount_rate=5,
                balance=0,
                name=f"{user.first_name}_{user.last_name}_account",
            )
            user.account = user_account
            if User.objects.all().count() <= 1:
                user.is_active = True
            else:
                user.is_active = False
            user.save()
            messages.success(request, "Registration Successful")
            return redirect("/index")
        else:
            error_message = "Please correct the following errors: {}".format(
                form.errors.as_text()
            )
            context = {"form": form, "perms": perms, "error_message": error_message}
            return render(request, "authentication/register.html", context)
    form = UserRegistrationForm()
    return render(
        request, "authentication/register.html", {"form": form, "perms": perms}
    )


def no_access_redirect(request):
    perms = get_user_permissions(request)
    user = request.user
    context = {"perms": perms, "user": user}
    return render(request, "authentication/no_access.html", context)


def elevate_user_view(request):
    perms = get_user_permissions(request)
    if perms not in ["3", "4"]:
        return redirect("no_access")

    if request.method == "POST":
        form = ElevateUserForm(request.POST)
        if form.is_valid():
            # Form is valid, process the data and return a response
            username = form.cleaned_data["user"]
            user = User.objects.get(username=username)
            group_name = form.cleaned_data["group"]
            print(user.groups.all())
            print(group_name)
            if group_name in user.groups.all():
                messages.error(request, "User is already in that group")
                context = {
                    "form": form,
                    "user": request.user,
                    "users": User.objects.filter(is_rep=False),
                    "perms": perms,
                }
                return render(request, "authentication/elevate_user.html", context)

            if group_name == "cinema_manager_temp":
                expiry_date_str = request.POST.get("expiry_date")
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                try:
                    group, created = Group.objects.get_or_create(name=group_name)
                except IntegrityError:
                    group = Group.objects.get(name=group_name)
                    created = False
                user.groups.add(group)
            else:
                try:
                    group, created = Group.objects.get_or_create(name=group_name)
                except IntegrityError:
                    group = Group.objects.get(name=group_name)
                    created = False
                user.groups.add(group)

            # Save changes to the user instance
            user.save()

            return redirect("index")
        else:
            print("invalid form")
    else:
        form = ElevateUserForm()

        context = {
            "form": form,
            "user": request.user,
            "users": User.objects.filter(is_rep=False),
            "perms": perms,
        }
        return render(request, "authentication/elevate_user.html", context)


def remove_user_from_group(request, pk, group):
    user = User.objects.get(pk=pk)
    group = Group.objects.get(pk=group)
    user.groups.remove(group)
    user.save()
    return redirect("user_management")
