from django.test import TestCase
from accounts.models import Account, UserAccount
from clubs.models import Club, ClubRepresentative
from authentication.models import User
from django.contrib.auth.models import Group
from django.urls import reverse

class AddClubTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", password="test")
        group, created = Group.objects.get_or_create(name="admin")
        user.groups.add(group)
        useraccount = UserAccount.objects.create(discount_rate=0.0, balance=20.0, name='User')
        user.account = useraccount
        user.save()
        clubrep = ClubRepresentative.objects.create(linked_user=user, representative_id='1', email="test@example.com", first_name="Club", last_name="Rep", password="password")
        acc = Account.objects.create(discount_rate=1.00, balance=0.05, name='John')
        club = Club.objects.create(name="Test Club", representative=clubrep, street_number=1, street="Test Road", city="Bristol", postcode="BS1 1AB", telephone_number="144755555", mobile_number="075555555", email_address="test@example.com", account=acc, active=True)

    # Test: create a new club & club rep
    # Expected result: new club & rep created with unique id and password
    def testClubCreated(self):
        self.client.post(reverse('create_club'), {'name':"Another Club", 'street_number':1, 'street':"Test Road", 'city':"Bristol", 'postcode':"BS1 1AB", 'telephone_number':"144755555", 'mobile_number':"075555555", 'email_address':"test@example.com"})
        newclub = Club.objects.get(name="Another Club")
        self.assertTrue(newclub)
        clubrep = ClubRepresentative.objects.get(representative_id="1")
        newclub.representative = clubrep
        self.assertEqual(newclub.representative, clubrep)   

    # Test: view list the list of clubs
    # Expected result: one club object found
    def testClubListView(self):
        response = self.client.get(reverse('clubs_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['clubs']), 1)

    # Test: view a single club (requires login)
    # Expected result: one club object found
    def testViewClub(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('view_club', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['club'])

    # Test: try to view a club without logging in
    # Expected result: no club view, client is redirected
    def testViewClubNoPerms(self):
        response = self.client.get(reverse('view_club', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.context, None)

    # Test: update a club
    # Expected result: club's name is changed, no club is found by the old name
    def testClubUpdated(self):
        response = self.client.post(reverse('update_club', args=[1]), {'name':"Altered Test Club", 'street_number':1, 'street':"Test Road", 'city':"Bristol", 'postcode':"BS1 1AB", 'telephone_number':"144755555", 'mobile_number':"075555555", 'email_address':"test@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Club.objects.filter(name="Altered Test Club")), 1)
        self.assertEqual(len(Club.objects.filter(name="Test Club")), 0)
    
    # Test: delete a club
    # Expected result: club no longer exists
    def testClubDeleted(self):
        response = self.client.post(reverse('delete_club', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Club.objects.filter()), 0)

    # Test: update a club rep's details
    # Expected result: club rep's name is changed, no rep is found by the old name
    def testRepUpdated(self):
        response = self.client.post(reverse('update_representative', args=[1]), {'email':"test@example.com", 'first_name':"Edited", 'last_name':"Rep", 'password':"password"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(ClubRepresentative.objects.filter(first_name="Edited")), 1)
        self.assertEqual(len(ClubRepresentative.objects.filter(first_name="Club")), 0)
