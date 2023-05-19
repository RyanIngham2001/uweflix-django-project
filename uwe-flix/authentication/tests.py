from django.test import TestCase
from accounts.models import UserAccount
from authentication.models import User
from clubs.models import ClubRepresentative
import datetime
from django.contrib.auth.models import Group
from django.urls import reverse

class AddAuthenticationTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", password="test")
        #group, created = Group.objects.get_or_create(name="admin")
        #user.groups.add(group)
        useraccount = UserAccount.objects.create(discount_rate=0.0, balance=20.0, name='User')
        user.account = useraccount
        user.save()
        clubrep = ClubRepresentative.objects.create(linked_user=user, representative_id='test', email="test@example.com", first_name="Club", last_name="Rep", password="test")

    # Test: no access redirect
    # Expected result: view is rendered
    def testNoAccessRedirect(self):
        response = self.client.post("/no_access/")
        self.assertEqual(response.status_code, 200)

    # Test: login with valid account details
    # Expected result: client logged in and redirected to index
    def testLogin(self):
        request = self.client.post(reverse('login'), {'inputUsername': 'test', 'inputPassword': 'test'})
        self.assertEqual(request.status_code, 302)

    # Test: login with invalid account details
    # Expected result: client not logged in and error returned
    def testInvalidLogin(self):
        request = self.client.post(reverse('login'), {'inputUsername': 'invalid', 'inputPassword': 'invalid'})
        self.assertEqual(request.status_code, 200)
        self.assertTrue(request.context['error'])
            
    # def testLogout(self):
    #    self.client.login(username="test", password="test")
    #    response = self.client.post(reverse('logout'))
    #    print(response.context)

#     #ERROR: doesn't successfully create a user
    def testRegistration(self):
       form = UserRegistrationForm(data={"email": "test@example.com", "username": "test1", "first_name": "Jim", "last_name": "Johnson", "date_of_birth": datetime.datetime(1999, 7, 13), "password1": "test", "password2": "test"})
       response = self.client.post("/register/", form=form)
       self.assertEqual(response.status_code, HTTPStatus.OK)
       self.assertEqual(User.objects.get(email="test@example.com").exists(),True)

    # Test: login with a club rep account
    # Expected result: client successfully logs in
    def testClubRepLogin(self):
       user = User.objects.get(username="test")
       user.is_rep = True
       request = self.client.post(reverse('club_rep_login'), {'inputUsername': 'test', 'inputPassword': 'test'})
       self.assertEqual(request.status_code, 302)

    # Test: try to login with incorrect details
    # Expected result: client is not logged in
    def testInvalidClubRepLogin(self):
        try:
            request = self.client.post(reverse('club_rep_login'), {'inputUsername': 'invalid', 'inputPassword': 'test'})
        except:
            pass
        else:
            self.assertTrue(False)

    # #ERROR: view didn't return an HttpResponse object
    def testUserElevation(self):
        self.client.login(username="test", password="test")
        response = self.client.post(reverse('elevate_user'), {"user": "test", "group": "admin"})
        user = User.objects.get(username="test")
        print(user.groups)
