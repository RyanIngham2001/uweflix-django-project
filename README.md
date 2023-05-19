UWEFlix Cinema Booking System Technical Documentation

Overview

The UWEFlix Cinema Booking System is a web-based application that enables students to purchase cinema tickets in advance of the showing via the internet. The system also allows university clubs to purchase blocks of tickets at discounted prices, make payments on account, and settle accounts monthly. The system must use the existing Payment Transaction System, and the privacy of all student and customer data must be assured. Additionally, the system must promote a sustainable, carbon-neutral approach to system performance in line with the UWE sustainability strategy.


Initial Setup


Clone the git repositry. Next run 'docker-compose up --build' in the root directory (that containes docker-compose.yml), this will create the Docker containers, images, and volume. Next run 'python manage.py loaddata initial_data.json' in the built-in docker terminal for the 'web' container to load some initial data files containing:

- Cinema
- Tickets
- Auth Groups
- Users:
       Account Manager
       
       Username: account_manager
       
       Cinema Manager
       
       Username: cinema_manager
       
       Admin
       
       Username: admin

The passwords are all: group5desd


Stripe API Login

Username: conor2.tainton@live.uwe.ac.uk

Password: group5desd


Goals and Requirements


Goals:


- Enable students to purchase cinema tickets in advance of the showing via the internet
- Enable university clubs to purchase blocks of tickets at discounted prices and make payments on account
- Requirements
- The system must use the existing Payment Transaction System.
- The user interface must be of high quality and accessible to UK and international students and those with mild visual impairments such as color blindness.
- The system must allow the Cinema Manager to register details of student clubs and their representatives, including club name, address details, and contact details.
- The system must allow the Cinema Manager to add film details, including title, age rating, duration, and short trailer description.
- The system must allow the Cinema Manager to delete details of an obsolete film if there are no showings allocated to it.
- The system must allow the Cinema Manager to add details of a new screen in the cinema, including the capacity of the screen in terms of the numbers of seats.
- The system must allow the Cinema Manager to add details of a new showing of a film, including the date and time of the showing.
- The system must allow the Account Manager to add a new account for a previously registered Club, including account details such as the account title, payment card details, and discount rate.
- The system must generate a unique account number for each account.
- The system must allow the Account Manager to amend an account and display a list of all accounts.
- The system must display account statements at the end of every calendar month.
- The system must allow customers to select a date and view a list of available showings for that date, including the time of the showings.
- The system must allow customers to view details of the showing, including film title, age rating, duration, and short trailer description.
- The system must allow customers to select the quantity of tickets required and the ticket type.
- The system must display the total cost of the booking.
- The system must allow customers to confirm their booking request.
- The system must allow customers to enter their payment card details and transact the payment via the existing Payment Transaction System.
- The system must allow Club Representatives to provide their club rep number and password for validation.
- The system must allow Club Representatives to nominate a date and view a list of available showings for that date, including the time of the showings.
- The system must allow Club Representatives to view details of the showing, including film title, age rating, duration, and short trailer description.
- The system must allow Club Representatives to select the quantity of tickets required, which must be no less than ten.
- The system must apply a student ticket type and club discount to the total cost of the block booking.
- The system must debit the total cost of the block booking from the club's account if there are sufficient seats available for the block booking.
- The system must allow Club Representatives to settle their accounts monthly by providing their unique club account number, displaying all transactions for the current month
- The system MUST provide appropriate data encryption and security measures to protect all customer and student data in compliance with GDPR and other legal requirements.
- The system MUST provide error handling and logging capabilities to help identify and resolve issues quickly and efficiently.
- The system MUST allow for easy and seamless integration with the existing Payment Transaction System to enable secure and reliable payment processing.
- The system MUST provide detailed reports on sales, revenue, and occupancy rates to enable UWEFlix to make informed business decisions and improve its operations.
- The system MUST be designed with scalability and modularity in mind to enable future enhancements and updates as needed.
- The system MUST provide adequate documentation and training resources to ensure that all users can effectively and efficiently use 
the system.

Overall, the UWEFlix Cinema Booking System must be designed and developed with the goal of providing a seamless and enjoyable experience for customers and club representatives while meeting the needs and requirements of all stakeholders, including the UWEFlix Management Team, student union stakeholders, the UWE student experience team, the UWEFlix Sales and Marketing team, and the UWEFlix Accounts Department. The system must be reliable, secure, scalable, and easy to use while also promoting sustainability and complying with all legal and regulatory requirements.


**Permission Levels**

The permission levels for the different roles (cinema manager and account manager) are defined in the 'auth_group' table of the database.

The Account manager role is assigned the group value of '1'.

The Cinema manager role is assigned the group value '2'.

These group values are assigned to users in the 'UWEFlix_user_groups' table.

A customer or club rep does not have a group value assigned in the 'UWEFlix_user_groups' table, resulting in a default of '0' in the views.py file, and no special permissions.

To mark club rep users as club reps, a marker is used in the 'UWEFlix_user' table under the field 'is_rep'. This field uses a value of '1' if the user is a club rep, and a value of '0' if the user is not a club rep.
