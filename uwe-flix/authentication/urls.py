from django.urls import path
from . import views

urlpatterns = [
    path("no_access/", views.no_access_redirect, name="no_access"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("club_rep_login/", views.club_rep_login, name="club_rep_login"),
    path("elevate_user/", views.elevate_user_view, name="elevate_user"),
    path(
        "remove_user_from_group/<int:pk>/<int:group>/",
        views.remove_user_from_group,
        name="remove_user_from_group",
    ),
]
