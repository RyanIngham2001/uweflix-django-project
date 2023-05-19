
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('create_cinema/', views.create_cinema, name="create_cinema"),

    path('manage_screens/', views.screen_list, name='manage_screens'),
    path('manage_screens/create_screen/', views.screen_create, name='create_screen'),
    path('manage_screens/update_screen/<int:pk>/', views.screen_update, name='update_screen'),
    path('manage_screens/delete_screen/<int:pk>/', views.screen_delete, name='delete_screen'),

    path('showings_management/', views.showings_list, name='showings_management'),
    path('showings_management/create_showing/', views.showing_create, name='create_showing'),
    path('showings_management/delete_showing/<int:pk>/', views.delete_showing, name='delete_showing'),
    path('showings_management/update_showing/<int:pk>/', views.update_showing, name='update_showing'),

    path('film_management/', views.films_list, name='film_management'),
    path('film_management/create_film/', views.film_create, name='create_film'),
    path('film_management/delete_film/<int:pk>/', views.film_delete, name='delete_film'),
    path('film_management/update_film/<int:pk>/', views.update_film, name='update_film'),
    
    path('showings_management/', views.showings_list, name='showings_management'),
    path('showings_management/delete_showing/<int:pk>/', views.delete_showing, name='delete_showing'),
    path('showings_management/update_showing/<int:pk>/', views.update_showing, name='update_showing'),

    path('user_management/',views.users_list, name="user_management"),
    path('user_management/enable_user/<int:pk>/',views.enable_user, name="enable_user"),
    path('user_management/disable_user/<int:pk>/',views.disable_user, name="disable_user"),

    path('ticket_management',views.tickets_list, name="ticket_management"),
    path('ticket_management/update_ticket/<int:pk>/',views.update_ticket, name="update_ticket"),

    path('cancellation_management/',views.bookings_list, name="cancellation_management"),
    path('cancellation_management/approve_cancellation/<int:pk>/',views.approve_cancellation, name="approve_cancellation"),
    path('cancellation_management/disapprove_cancellation/<int:pk>/',views.disapprove_cancellation, name="disapprove_cancellation"),
]
