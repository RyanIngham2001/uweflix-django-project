from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import User
from django.contrib import messages
from django.conf import settings
from utils.custom_decorators import get_user_permissions, is_in_group
from utils.create_statement import create_statement
from .forms import AccountForm, EndOfMonthStatementForm, TopUpForm, StudentDiscountForm
from .models import (
    Account,
    EndOfMonthStatement,
    UserAccount,
    CinemaAccount,
    ClubAccount,
    StudentDiscountRequest,
    TopUpStripeInformation,
    TransactionHistory,
)
from clubs.models import ClubRepresentative
from .serialisers import TopUpStripeInformationSerializer
from clubs.models import Club
from decimal import Decimal
import requests
from rest_framework import status
import datetime


# Create your views here.


def accounts_list(request):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    club_accounts = ClubAccount.objects.all()
    user_accounts = UserAccount.objects.all()
    cinema_accounts = CinemaAccount.objects.all()
    context = {
        "club_accounts": club_accounts,
        "user_accounts": user_accounts,
        "cinema_accounts": cinema_accounts,
        "perms": perms,
    }
    return render(request, "accounts/accounts_list.html", context)


def account_create(request):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    clubs = Club.objects.all()
    ### USER SUBMITS FORM ###
    if not request.user.groups.all().filter(name="account_manager").exists():
        print(request.user.user_permissions)
        return redirect("no_access")

    if request.method == "POST":
        # code to handle form submission and create a new account
        form = AccountForm(request.POST)
        print(form.errors)
        if form.is_valid():
            account = form.save(commit=True)
            club = form.cleaned_data["club"]
            club.account = account
            club.save()
            return redirect("accounts_list")
        else:
            # render the form with errors
            context = {
                "form": form,
                "user": request.user,
                "clubs": clubs,
                "perms": perms,
            }
            return render(request, "accounts/create_account.html", context)
    else:
        ### USER REQUESTS FORM ###
        # render the empty form
        form = AccountForm()
        context = {"form": form, "user": request.user, "clubs": clubs, "perms": perms}
        return render(request, "accounts/create_account.html", context)


def account_update(request, pk):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        # Check if the form is valid
        if form.is_valid():
            # Save the form and redirect to the club list page
            form.save()
            return redirect("accounts_list")
    # If the request is not POST, or the form is invalid,
    # render the update page with the club instance and the form
    form = AccountForm(instance=account)
    context = {
        "form": form,
        "user": request.user,
        "account": account,
        "pk": pk,
        "perms": perms,
    }
    return render(request, "accounts/update_account.html", context)


def account_delete(request, pk):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    account = get_object_or_404(Account, pk=pk)
    account.delete()
    return redirect("accounts_list")


def statements_list(request, pk):
    perms = get_user_permissions(request)
    if perms == "0" or perms == "1":
        return redirect("no_access")

    account = Account.objects.get(pk=pk)
    statements = EndOfMonthStatement.objects.filter(account__pk=pk)
    print(f"statements: {statements}")
    context = {"user": request.user, "statements": statements, "perms": perms}
    return render(request, "accounts/manage_statements.html", context)


def statement_generate(request, pk):
    perms = get_user_permissions(request)
    if perms == "0" or perms == "1":
        return redirect("no_access")

    account = Account.objects.get(pk=pk)
    statement = create_statement(account_id=pk)
    statement.save()

    statements = EndOfMonthStatement.objects.filter(account__pk=pk)
    context = {"user": request.user, "statements": statements, "perms": perms}
    return render(request, "accounts/manage_statements.html", context)


def statement_update(request, pk, st_pk):
    perms = get_user_permissions(request)
    if perms == "0" or perms == "1":
        return redirect("no_access")

    account = Account.objects.get(pk=pk)
    statement = EndOfMonthStatement.objects.get(pk=st_pk)
    statements = EndOfMonthStatement.objects.filter(account__pk=pk)

    if request.method == "POST":
        form = EndOfMonthStatementForm(request.POST, instance=statement)
        # Check if the form is valid
        if form.is_valid():
            # Save the form and redirect to the club list page
            amended_statement = form.save()
            new_outstanding = EndOfMonthStatement.update_outstanding(
                amended_statement.id
            )
            amended_statement.outstanding = new_outstanding
            amended_statement.save()

            context = {"user": request.user, "statements": statements, "perms": perms}
            return render(request, "accounts/manage_statements.html", context)
    # If the request is not POST, or the form is invalid,
    # render the update page with the club instance and the form
    form = EndOfMonthStatementForm(instance=statement)
    context = {
        "form": form,
        "user": request.user,
        "account": account,
        "pk": pk,
        "st_pk": st_pk,
        "statement": statement,
        "perms": perms,
    }
    return render(request, "accounts/update_statement.html", context)


def debit_history(request, pk, config):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    account = get_object_or_404(Account, pk=pk)
    customer_id = account.stripeCustomerID
    transactions = []

    # Check if customer_id is TBD. This will indicate that no transactions have ever been made
    if customer_id == "TBD" or customer_id == "":
        transactions.append(
            TransactionHistory(
                "NO TRANSACTION HISTORY",
                "",
                "",
                "",
            )
        )

    else:
        response = requests.post(
            "http://stripe:8001/api/top_up_history/",
            data={"config": config, "customer_id": customer_id},
        )
        response_dict = response.json()

        payment_history_json = response_dict["payment_history"]

        for payment in payment_history_json["data"]:
            transactions.append(
                TransactionHistory(
                    payment["id"],
                    Decimal(payment["amount"] / 100),
                    datetime.datetime.fromtimestamp(payment["created"]),
                    payment["status"],
                )
            )

    context = {"user": request.user, "perms": perms, "transactions": transactions}

    return render(request, "accounts/debit_history.html", context)


def credit_history(request, pk, config):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    return render(request, "accounts/credit_history.html")


def statement_delete(request, pk, st_pk):
    perms = get_user_permissions(request)
    if not perms == "2" and not perms == "4":
        return redirect("no_access")

    account = Account.objects.get(pk=pk)
    statement = EndOfMonthStatement.objects.get(pk=st_pk)
    statement.delete()
    statements = EndOfMonthStatement.objects.filter(account__pk=pk)
    context = {"user": request.user, "statements": statements, "perms": perms}
    return render(request, "accounts/manage_statements.html", context)


# Handle making a top-up request into a checkout session with the Stripe API
def top_up_request(request, pk, account, amount):
    customer_id = account.stripeCustomerID

    topup_item = TopUpStripeInformation(
        "Top-Up Balance",
        "Amount to top-up UWEFlix Account with",
        int(Decimal(amount) * 100),
        1,
        customer_id,
    )

    serializer = TopUpStripeInformationSerializer(topup_item)

    response = requests.post(
        "http://stripe:8001/api/top_up_create_checkout_session/",
        json=serializer.data,
    )
    response_dict = response.json()

    # If checkout session was created and processed
    if response.status_code == status.HTTP_201_CREATED:
        account.stripeCustomerID = response_dict["customerID"]
        account.save()

        # Update the account balance NEEDS TO BE MOVED TO WEBHOOK SUCCESS OF PAYMENT
        account.balance += Decimal(amount)
        account.save()

        messages.success(
            request, f"{amount} was successfully added to your account balance."
        )

        return "Success", response_dict

    else:
        messages.error(request, "Error occurred creating checkout.")
        return "Error", response_dict


# Handle a request from a student or staff member to top-up the account of the club
def top_up_balance(request, pk):
    perms = get_user_permissions(request)
    user = request.user
    if user.is_rep == True or perms == "-1":
        return redirect("no_access")

    account = get_object_or_404(Account, pk=pk)

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = request.POST.get("amount")

            account = get_object_or_404(Account, pk=pk)

            response, response_dict = top_up_request(request, pk, account, amount)

            if response == "Success":
                return redirect(response_dict["url"])

            else:
                return render(request, "accounts/top_up_balance.html", context)

    form = TopUpForm()
    context = {"user": request.user, "perms": perms, "form": form}

    return render(request, "accounts/top_up_balance.html", context)


# Handle a request from a club rep to top-up the account of the club
def top_up_club_balance(request, pk):
    perms = get_user_permissions(request)
    user = request.user

    if not user.is_rep == True or perms == "-1":
        return redirect("no_access")

    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = request.POST.get("amount")

            club_representative = ClubRepresentative.objects.get(linked_user=user)
            club = Club.objects.get(representative=club_representative.id)
            account = club.account

            response, response_dict = top_up_request(request, pk, account, amount)

            if response == "Success":
                return redirect(response_dict["url"])

            else:
                return render(request, "accounts/top_up_balance.html", context)

    form = TopUpForm()
    context = {"user": request.user, "perms": perms, "form": form}
    return render(request, "accounts/top_up_balance.html", context)


def create_student_discount_request(request, pk):
    perms = get_user_permissions(request)
    if request.method == "POST":
        student = User.objects.get(pk=pk)
        form = StudentDiscountForm(request.POST)
        if form.is_valid():
            student_discount_request = form.save(commit=False)
            student_discount_request.student = student
            student_discount_request.old_discount_rate = student.account.discount_rate
            student_discount_request.save()
            return redirect("index")
    else:
        form = StudentDiscountForm()
    return render(
        request,
        "accounts/create_student_discount_request.html",
        {"perms": perms, "form": form},
    )


def approve_student_discount_request(request, pk):
    perms = get_user_permissions(request)
    if perms == "0" or perms == "1":
        return redirect("no_access")
    discount_request = get_object_or_404(StudentDiscountRequest, pk=pk)
    student = discount_request.student
    student.account.discount_rate = discount_request.new_discount_rate
    student.account.save()
    discount_request.delete()
    return redirect("user_management")


def deny_student_discount_request(request, pk):
    perms = get_user_permissions(request)
    if perms == "0" or perms == "1":
        return redirect("no_access")
    discount_request = get_object_or_404(StudentDiscountRequest, pk=pk)
    discount_request.delete()
    return redirect("user_management")
