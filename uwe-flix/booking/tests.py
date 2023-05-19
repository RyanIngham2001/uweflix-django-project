from django.test import TestCase
from accounts.models import UserAccount
from authentication.models import User
from booking.models import *
from cinema.models import *
import datetime
from django.utils import timezone
from django.urls import reverse

class AddBookingTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", password="test")
        #group, created = Group.objects.get_or_create(name="admin")
        #user.groups.add(group)
        useraccount = UserAccount.objects.create(discount_rate=0.0, balance=20.0, name='User')
        user.account = useraccount
        user.save()
        cinema = Cinema.objects.create(name="Cinema", location="Bristol")
        screen = Screen.objects.create(cinema=cinema, screen_number=2, seating_capacity=100)
        film = Film.objects.create(title="Film1", length=datetime.timedelta(hours=2), rating=12, genre="Comedy", poster_url="www.example.com/image.webp")
        showing = Showing.objects.create(screen=screen, film=film, start_time=timezone.now(), available_seats=100)
        Ticket.objects.create(ticket_type="Adult Ticket", price=10)
        Ticket.objects.create(ticket_type="Student Ticket", price=7.5)
        Ticket.objects.create(ticket_type="Child Ticket", price=5)

    # Test: purchase advance tickets
    # Expected result: reservation object created, funds processed
    def testPurchaseTicket(self):
        self.client.login(username="test", password="test")
        request = self.client.post(reverse('make_booking'),{'showing': 1, 'student_quantity':0, 'adult_quantity': 1, 'child_quantity': 0})
        self.assertEqual(request.status_code, 200)
        #print(request.context)
        self.assertEqual(len(Reservation.objects.filter()), 1)

    # Test: attempt to purchase a ticket when there are insufficient seats
    # Expected result: booking request is not accepted
    #def testPurchaseTicketInsufficientSeats(self):
    #    pass

    # Test: purchase multiple tickets for a club
    # Expected result: multiple tickets purchased and club account debited
    #def testPurchaseBlockTickets(self):
    #    pass

    # make_specific_booking

    # view_bookings

    # request_cancellation