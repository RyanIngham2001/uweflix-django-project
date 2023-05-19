from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from utils.custom_decorators import get_user_permissions, is_in_group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from authentication.models import User
from .models import Club, ClubRepresentative, ClubDiscountRequest
from .forms import ClubForm, ClubRepresentativeForm, ClubDiscountRequestForm
from accounts.models import Account, ClubAccount
import random
import datetime

# Create your views here.

def clubs_list(request):
    perms = get_user_permissions(request)
    if not perms == '3' and not perms == '4':
        return redirect('no_access')
    
    clubs = Club.objects.filter(active=True)
    clubs_for_approval = Club.objects.filter(active=False)
    discount_requests = ClubDiscountRequest.objects.filter(approved=False)
    accounts = ClubAccount.objects.all()
    #representatives = User.objects.all().filter(club_rep=True)
    context = {'user': request.user, 'clubs': clubs, 'inactive_clubs': clubs_for_approval,'accounts': accounts, 'discount_requests': discount_requests, 'perms': perms}
    return render(request, 'clubs/manage_clubs.html', context)

@login_required
def view_club(request, pk):
    perms = get_user_permissions(request)
    if perms == '2' or perms == '3' or perms == '4':
        if pk == 9999999:
            try:
                representative = ClubRepresentative.objects.get(linked_user=request.user)
                club = Club.objects.get(representative=representative)
            except ClubRepresentative.DoesNotExist:
                return redirect("no_access/")
        else:
            club = get_object_or_404(Club, pk=pk)
            representative=club.representative
        context = {
            'club': club,
            'representative': representative,
        }
        
        return render(request, 'clubs/view_club.html', context)
            
def activate_club(request, pk):
    perms = get_user_permissions(request)

    if not perms == '3' and not perms == '4':
        return redirect('no_access')
    
    club = Club.objects.get(pk=pk)
    club.active = True
    club.save()

    club_representative = ClubRepresentative.objects.get(pk=club.representative_id)
    representative = User.objects.get(pk=club_representative.linked_user_id)
    representative.is_active = True
    representative.save()

    return redirect('clubs_list')

def deactivate_club(request, pk):
    perms = get_user_permissions(request)

    if not perms == '3' and not perms == '4':
        return redirect('no_access')
    
    club = Club.objects.get(pk=pk)
    club.active = False
    club.save()

    club_representative = ClubRepresentative.objects.get(pk=club.representative_id)
    representative = User.objects.get(pk=club_representative.linked_user_id)
    representative.is_active = False
    representative.save()

    return redirect('clubs_list')


def club_update(request, pk):
    perms = get_user_permissions(request)
    if not perms == '3' and not perms == '4':
        return redirect('no_access')
    
    club = get_object_or_404(Club, pk=pk)

    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the form with the POST data
        form = ClubForm(request.POST, instance=club)
        # Check if the form is valid
        if form.is_valid():
            # Save the form and redirect to the club list page
            form.save(commit=True)
            return redirect('clubs_list')
    # If the request is not POST, or the form is invalid,
    # render the update page with the club instance and the form
    form = ClubForm(instance=club)
    context = {'form': form, 'club': club, 'pk': pk, 'perms': perms}
    return render(request, 'clubs/update_club.html', context)


def club_delete(request, pk):
    perms = get_user_permissions(request)
    
    if not perms == '3' and not perms == '4':
        return redirect('no_access')
    
    club = get_object_or_404(Club, pk=pk)
    # Get the representative and account associated with the club
    representative = club.representative
    account = club.account
    # Delete the club
    club.delete()
    # Delete the representative and account
    representative.delete()
    account.delete()
    return redirect('clubs_list')


def club_create(request):
    perms = get_user_permissions(request)

    if not perms == '-1' and not perms == '4':
        return redirect('no_access')

    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=True)
            club.is_active = False
            representative_id = club.name[0] + str(random.randint(1,1000))
            club_rep_user = User.objects.create(username=representative_id, password=make_password(representative_id), is_rep=True)
            club_rep = ClubRepresentative.objects.create(linked_user = club_rep_user, representative_id=representative_id)
            club_rep.is_rep=True
            club_rep.is_active=False
            club_rep.save()
            account_name = club.name + ' account'
            club_account = ClubAccount.objects.create(discount_rate=0, balance=0, name=account_name)
            
            club.representative = club_rep
            club.account = club_account
            club.save()
            messages.success(request, 'Club created successfully.')
            return redirect('/index/')
        else:
            messages.error(request, 'There was an error creating the club')
    else:
        form = ClubForm()
    context = {'form': form, 'user': request.user, 'perms': perms}
    return render(request, 'clubs/create_club.html', context)

def representative_update(request, pk):
    perms = get_user_permissions(request)
    if not perms == '3' and not perms == '4':
        return redirect('no_access')
    
    club = get_object_or_404(Club, pk=pk)
    representative = club.representative
    if request.method == 'POST':
        print('request post')
        form = ClubRepresentativeForm(request.POST, instance=representative)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            representative.linked_user.set_password(make_password(password))
            representative.linked_user.save()
            form.save(commit=True)
            return redirect('clubs_list')
        else:
            print(form.errors)
    else:
        form = ClubRepresentativeForm(instance=representative, initial={'representative_id': representative.representative_id})
    context = {'form': form, 'user': request.user, 'club': club, 'representative': representative, 'perms': perms}
    return render(request, 'clubs/update_representative.html', context)

def create_club_discount_request(request, pk):
    perms = get_user_permissions(request)
    if not perms == '1' and not perms == '4':
        return redirect('no_access')
    
    if request.method == 'POST':
        club = get_object_or_404(Club, pk=pk)
        form = ClubDiscountRequestForm(request.POST)
        if form.is_valid():
            club_discount_request = form.save(commit=False)
            club_discount_request.club = club
            club_discount_request.old_discount_rate = club.account.discount_rate
            club_discount_request.save()
            return redirect('index') 
    else:
        form = ClubDiscountRequestForm()
    return render(request, 'clubs/create_club_discount_request.html', {'perms': perms, 'form': form})

def approve_club_discount_request(request, pk):
    perms = get_user_permissions(request)
    if not perms == '3' and not perms == '4':
        return redirect('no_access')

    discount_request = get_object_or_404(ClubDiscountRequest, pk=pk)
    club = discount_request.club
    club.account.discount_rate = discount_request.discount_rate
    club.account.save()
    discount_request.delete()
    return redirect('clubs_list')

def deny_club_discount_request(request, pk):
    perms = get_user_permissions(request)
    if not perms == '3' and not perms == '4':
        return redirect('no_access')  
    
    discount_request = get_object_or_404(ClubDiscountRequest, pk=pk)
    discount_request.delete()
    return redirect('clubs_list')