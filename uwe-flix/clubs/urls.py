
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('create_club/', views.club_create, name='create_club'),
    path('manage_clubs/', views.clubs_list, name='clubs_list'),
    path('manage_clubs/<int:pk>/update', views.club_update, name='update_club'),
    path('manage_clubs/<int:pk>/delete', views.club_delete, name='delete_club'),
    path('manage_clubs/<int:pk>/update_representative/', views.representative_update, name='update_representative'),
    path('view_club/<int:pk>/', views.view_club, name='view_club'),
    path('deactivate_club/<int:pk>/', views.deactivate_club, name='deactivate_club'),
    path('activate_club/<int:pk>/', views.activate_club, name='activate_club'),
    path('create_club_discount_request/<int:pk>/', views.create_club_discount_request, name='create_club_discount_request'),
    path('approve_club_discount_request/<int:pk>/', views.approve_club_discount_request, name='approve_club_discount_request'),
    path('deny_club_discount_request/<int:pk>', views.deny_club_discount_request, name='deny_club_discount_request'),
]
