from django.test import TestCase
from accounts.models import *
from authentication.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
import datetime

class AddAccountTests(TestCase):   
    def setUp(self):
        user = User.objects.create_user(username="test", password="test")
        group, created = Group.objects.get_or_create(name="account_manager")
        user.groups.add(group)
        useraccount = UserAccount.objects.create(discount_rate=0.0, balance=20.0, name='User')
        user.account = useraccount
        user.save()

        acc = Account.objects.create(discount_rate=1.00, balance=0.05, name='John')
        EndOfMonthStatement.objects.create(account=acc, total_spent=1.00, total_paid=0.5, outstanding=0.5)
        StudentDiscountRequest.objects.create(student=user, old_discount_rate=0.0, new_discount_rate=1.0, reason="Test", approved=False)

    # Test: view the list of accounts
    # Expected result: three account objects found
    def testAccountListView(self):
        UserAccount.objects.create(discount_rate=2.00, balance=5.00, name='Jim')
        UserAccount.objects.create(discount_rate=1.50, balance=10.50, name='Jeff')
        response = self.client.get(reverse('accounts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['user_accounts']), 3)

    # NOT NULL contraint failed: accounts_account.balance
    # Test: create a new account
    # Expected result: new account created with unique id
    def testAccountCreated(self):
        self.client.login(username="test", password="test")
        response = self.client.post(reverse('create_account'), {'discount_rate': 2.00})
        self.assertEqual(response.status_code, 200)
        print(response.context)

    # Test: update an existing account
    # Expected result: account's discount rate is changed
    def testAccountUpdated(self):
        response = self.client.post(reverse('update_account', args=[2]), {'discount_rate': 3.00})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.get(name="John").discount_rate, 3.00)

    # Test: delete an account
    # Expected result: account no longer exists
    def testAccountDeleted(self):
       self.assertEqual(len(Account.objects.filter()), 2)
       response = self.client.post(reverse('delete_account', args=[2]))
       self.assertEqual(response.status_code, 302)
       self.assertEqual(len(Account.objects.filter()), 1)

    # Test: view list the list of statements
    # Expected result: three statement objects found
    def testStatementListView(self):
        acc = Account.objects.get(id=1)
        EndOfMonthStatement.objects.create(account=acc, total_spent=5.00, total_paid=2.5, outstanding=2.5)
        EndOfMonthStatement.objects.create(account=acc, total_spent=10.00, total_paid=10.00, outstanding=0.0)
        response = self.client.get(reverse('manage_statements', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(EndOfMonthStatement.objects.filter()), 3)

    # Test: generate a new statement
    # Expected result: one more statement object found
    def testStatementGenerated(self):
        response = self.client.post(reverse('generate_statement', args=[2]), {'total_spent': 2.00, 'total_paid': 1.00, 'outstanding': 1.00})
        self.assertEqual(len(EndOfMonthStatement.objects.filter()), 2)

    # DOES NOT CURRENTLY PASS
    # Test: update an existing statement
    # Expected result: statement details are altered
    def testStatementUpdated(self):
        response = self.client.post(reverse('update_statement', args=[2,1]), {'date': datetime.date.today, 'total_spent': 1.00, 'total_paid': 1.00, 'outstanding': 0.00})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(EndOfMonthStatement.objects.filter(outstanding=0.00)), 1)
        self.assertEqual(len(EndOfMonthStatement.objects.filter(outstanding=0.5)), 0)
    
    # Test: delete a statement
    # Expected result: no statements found
    def testStatementDeleted(self):
        response = self.client.post(reverse('delete_statement', args=[2,1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(EndOfMonthStatement.objects.filter()), 0)

    # CURRENTLY DOES NOT WORK: paymentConfirm is not a valid url
    # Test: top up an account's balance
    # Expected result: the account's balance is increased by 10
    def testTopUpBalance(self):
        #self.client.login(username="test", password="test")
        acc = Account.objects.get(id=1)
        response = self.client.post(reverse('top_up_balance', args=[1]), {'amount':10.00, 'cardNumber':'1234567812345678', 'expiryMonth': 12, 'expiry_year': 3000, 'cvc': '123', 'cardHolderName': 'Mr Test'})
        self.assertEqual(acc.balance, 30)

    # AttributeError: 'Settings' object has no attribute 'USER_AUTH_MODEL'
    # Test: create a student discount request
    # Expected result: new student discount request object is created
    def testStudentDiscountRequestCreated(self):
        acc = Account.objects.get(id=1)
        request = self.client.post(reverse('create_student_discount_request', args=[1]), {'new_discount_rate': 5.0, 'reason': 'Test'})
        self.assertEqual(len(StudentDiscountRequest.objects.filter()), 2)

    # Test: approve a student discount request
    # Expected result: request is approved and deleted, user's discount rate is changed
    def testApproveStudentDiscountRequest(self):
        response = self.client.post(reverse('approve_student_discount_request', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(StudentDiscountRequest.objects.filter()), 0)
        self.assertEqual(UserAccount.objects.get(id=1).discount_rate, 1.00)

    # DOES NOT WORK: deny_student_discount_request is not implemented
    # Test: deny a student discount request
    # Expected result: request is denied and deleted, user's discount rate is unchanged
    def testDenyStudentDiscountRequest(self):
        request = self.client.post(reverse('deny_student_discount_request', args=[1]))
        self.assertEqual(len(StudentDiscountRequest.objects.filter()), 1)
        self.assertEqual(UserAccount.objects.get(id=1).discount_rate, 0.00)