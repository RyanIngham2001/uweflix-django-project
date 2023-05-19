from django.contrib.auth import get_user_model
from authentication.models import User
from clubs.models import Club, ClubRepresentative

def club_account_balance(request):
    user = request.user
    if user.is_authenticated:
        if user.is_rep == True:
            club_representative = ClubRepresentative.objects.get(linked_user=user)
            club = Club.objects.get(representative=club_representative.id)
            account = club.account
            print (account.balance)
            return {'club_account_balance': account.balance}
    return {}