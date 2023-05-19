from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.accounts_list, name="accounts_list"),
    path("accounts/create_account/", views.account_create, name="create_account"),
    path(
        "accounts/<int:pk>/update_account/", views.account_update, name="update_account"
    ),
    path(
        "accounts/<int:pk>/delete_account/", views.account_delete, name="delete_account"
    ),
    path(
        "accounts/<int:pk>/manage_statements/",
        views.statements_list,
        name="manage_statements",
    ),
    path(
        "accounts/<int:pk>/generate_statement/",
        views.statement_generate,
        name="generate_statement",
    ),
    path(
        "accounts/<int:pk>/manage_statements/<int:st_pk>/update/",
        views.statement_update,
        name="update_statement",
    ),
    path(
        "accounts/<int:pk>/manage_statements/<int:st_pk>/delete/",
        views.statement_delete,
        name="delete_statement",
    ),
    path(
        "accounts/<int:pk>/top_up_balance/", views.top_up_balance, name="top_up_balance"
    ),
    path(
        "accounts/<int:pk>/top_up_club_balance/",
        views.top_up_club_balance,
        name="top_up_club_balance",
    ),
    path(
        "accounts/create_student_discount_request/<int:pk>/",
        views.create_student_discount_request,
        name="create_student_discount_request",
    ),
    path(
        "accounts/approve_student_discount_request/<int:pk>/",
        views.approve_student_discount_request,
        name="approve_student_discount_request",
    ),
    path(
        "accounts/deny_student_discount_request/<int:pk>/",
        views.deny_student_discount_request,
        name="deny_student_discount_request",
    ),
    path(
        "accounts/debit_history/<int:pk>/<int:config>/",
        views.debit_history,
        name="debit_history",
    ),
    path(
        "accounts/credit_history/<int:pk>/<int:config>/",
        views.credit_history,
        name="credit_history",
    ),
]
