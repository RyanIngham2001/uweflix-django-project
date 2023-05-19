from django.test import TestCase
from accounts.models import UserAccount
from booking.models import Reservation, Cancelation
from authentication.models import User
from django.contrib.auth.models import Group
from cinema.models import *
import datetime
from django.urls import reverse
from django.utils import timezone

class AddCinemaTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", password="test")
        group, created = Group.objects.get_or_create(name="cinema_manager")
        user.groups.add(group)
        useraccount = UserAccount.objects.create(discount_rate=0.0, balance=20.0, name='User')
        user.account = useraccount
        user.save()
        #self.client.login(username="test", password="test")
        cinema = Cinema.objects.create(name="Cinema", location="Bristol")
        screen = Screen.objects.create(cinema=cinema, screen_number=1, seating_capacity=100)
        film = Film.objects.create(title="Film1", length=datetime.timedelta(hours=2), rating=12, genre="Comedy", poster_url="www.example.com/image.webp")
        tz = timezone.get_current_timezone()
        showing = Showing.objects.create(screen=screen, film=film, start_time=datetime.datetime(2023, 12, 1, 11, 30, 0, tzinfo=tz), available_seats=200)
        reservation = Reservation.objects.create(showing=showing, student_quantity=0, adult_quantity=1, child_quantity=0, booking_cost=10.0, reservee=user)
        Cancelation.objects.create(reservation=reservation)

    # CURRENTLY DOES NOT WORK
    # Test: add a new cinema
    # Expected result: new cinema object added to the system
    # def testCinemaCreated(self):
    #     self.client.login(username="test", password="test")
    #     response = self.client.post(reverse('create_cinema'), {'name': 'Cinema 2', 'location': 'Bristol'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(len(Cinema.objects.filter(name='Cinema 2')), 1)

    # Test: view the list of screens through the 'manage_screens' url
    # Expected result: three screen objects found
    def testManageScreens(self):
        cinema = Cinema.objects.get(id=1)
        Screen.objects.create(cinema=cinema, screen_number=2, seating_capacity=100)
        Screen.objects.create(cinema=cinema, screen_number=3, seating_capacity=100)
        response = self.client.get(reverse('manage_screens'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['screens']), 3)

    # Test: add a new screen
    # Expected result: new object added to the system
    def testScreenCreated(self):
        response = self.client.post(reverse('create_screen'), {'cinema': 1, 'screen_number': 2, 'seating_capacity': 100})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Screen.objects.filter(screen_number=2)), 1)

    # Test: update an existing screen
    # Expected result: screen's seating capacity is changed
    def testScreenUpdated(self):
        response = self.client.post(reverse('update_screen', args=[1]), {'cinema': 1, 'screen_number': 1, 'seating_capacity': 300})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Screen.objects.get(screen_number=1).seating_capacity, 300)

    # Test: delete a screen
    # Expected result: screen no longer exists
    def testScreenDeleted(self):
       self.assertEqual(len(Screen.objects.filter()), 1)
       response = self.client.post(reverse('delete_screen', args=[1]))
       self.assertEqual(response.status_code, 302)
       self.assertEqual(len(Screen.objects.filter()), 0) 

    # Test: view the list of screens through the 'screen_list' url
    # Expected result: three screen objects found
    def testScreenListView(self):
        cinema = Cinema.objects.get(id=1)
        Screen.objects.create(cinema=cinema, screen_number=2, seating_capacity=100)
        Screen.objects.create(cinema=cinema, screen_number=3, seating_capacity=100)
        response = self.client.get(reverse('screen_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['screens']), 3)  

    # Test: add a new showing
    # Expected result: new showing object added to the system
    def testShowingCreated(self):
        response = self.client.post(reverse('create_showing'), {'screen':Screen.objects.get(screen_number=1).id, 'film':Film.objects.get(title="Film1").id, 'start_time':"0023-04-24 16:44:00", 'social_distancing': False})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Showing.objects.filter()), 2)

    # Test: add a new film
    # Expected result: new film object added to the system
    def testFilmCreated(self):
        response = self.client.post(reverse('create_film'), {'title': 'A Film', 'length': 60, 'rating': "PG", "genre": "Comedy"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Film.objects.filter(title="A Film")), 1)

    # Test: view the list of films
    # Expected result: three film objects found
    def testFilmListView(self):
        Film.objects.create(title="Film2", length=datetime.timedelta(hours=2), rating=12, genre="Comedy", poster_url="www.example.com/image.webp")
        Film.objects.create(title="Film3", length=datetime.timedelta(hours=2), rating=12, genre="Comedy", poster_url="www.example.com/image.webp")
        response = self.client.post(reverse('film_management'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['films']), 3)
    
    # Test: delete a film
    # Expected result: film no longer exists
    def testFilmDeleted(self):
       self.assertEqual(len(Film.objects.filter()), 1)
       response = self.client.post(reverse('delete_film', args=[1]))
       self.assertEqual(response.status_code, 302)
       self.assertEqual(len(Film.objects.filter()), 0)   

    # CURRENTLY DOESN'T WORK (because update_film isn't fully implemented)
    # Test: update an existing film
    # Expected result: film's title is changed
    def testFilmUpdated(self):
        response = self.client.post(reverse('update_film', args=[1]), {'title': 'Film2', 'length': 120, 'rating': "12", "genre": "Comedy"})
        self.assertEqual(response.status_code, 302)
        print(response.context)
        print(Film.objects.get(id=1).title)
    
    # Test: view the list of showings for a film
    # Expected result: three showing objects found
    def testFilmShowings(self):
        screen = Screen.objects.get(id=1)
        film = Film.objects.get(id=1)
        tz = timezone.get_current_timezone()
        Showing.objects.create(screen=screen, film=film, start_time=datetime.datetime(2023, 12, 1, 11, 30, 0, tzinfo=tz), available_seats=200)
        Showing.objects.create(screen=screen, film=film, start_time=datetime.datetime(2023, 12, 1, 11, 30, 0, tzinfo=tz), available_seats=200)
        response = self.client.post(reverse('film_showings', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['showings']), 3)

    # showings_management

    # Test: delete a showing
    # Expected result: showing no longer exists
    def testShowingDeleted(self):
       self.assertEqual(len(Showing.objects.filter()), 1)
       response = self.client.post(reverse('delete_showing', args=[1]))
       self.assertEqual(response.status_code, 302)
       self.assertEqual(len(Showing.objects.filter()), 0) 

    # ERROR: doesn't update details but redirects to manage_screens which implies it was successful
    # check is update_showing even works
    # Test: update an existing showing
    # Expected result: showing's time is changed
    def testShowingUpdated(self):
        self.client.login(username="test", password="test")
        tz = timezone.get_current_timezone()
        newtime = datetime.datetime(2023, 12, 1, 12, 45, 0, tzinfo=tz)
        response = self.client.post(reverse('update_showing', args=[1]), {'screen':Screen.objects.get(screen_number=1).id, 'film':Film.objects.get(title="Film1").id, 'start_time':"0023-04-24 16:44:00", 'social_distancing': False})
        self.assertEqual(response.status_code, 302)
        print(response)
        self.assertEqual(Showing.objects.get(id=1).start_time, newtime)

    # Test: view the list of users
    # Expected result: three user objects found
    def testUserListView(self):
        User.objects.create_user(username="test2", password="test")
        User.objects.create_user(username="test3", password="test")
        response = self.client.post(reverse('user_management'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 3)

    # enable_user

    # disable_user  

    # Test: view the list of tickets
    # Expected result: three ticket objects found
    def testTicketListView(self):
        Ticket.objects.create(ticket_type="Adult Ticket", price=10)
        Ticket.objects.create(ticket_type="Student Ticket", price=7.5)
        Ticket.objects.create(ticket_type="Child Ticket", price=5)
        response = self.client.post(reverse('ticket_management'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tickets']), 3)

    # update_ticket

    # Test: view the list of cancellations
    # Expected result: three cancellation objects found
    def testBookingListView(self):
        reservation = Reservation.objects.get(id=1)
        Cancelation.objects.create(reservation=reservation)
        Cancelation.objects.create(reservation=reservation)
        response = self.client.post(reverse('cancellation_management'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cancellations']), 3)

    # approve_cancellation

    # disapprove_cancellation

    # manage_tickets