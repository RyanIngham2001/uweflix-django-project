from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta

# Create your models here.


class Cinema(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    ageRatings = [
        ("U", "U"),
        ("PG", "PG"),
        ("12", "12"),
        ("15", "15"),
        ("18", "18"),
    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    length = models.DurationField()
    rating = models.CharField(max_length=3, choices=ageRatings, default="U")
    description = models.CharField(max_length=255, default="")
    poster_url = models.CharField(max_length=255, default="")
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def archive(self):
        self.archived = True
        self.save()
        return self

    def unarchive(self):
        self.archived = False
        self.save()
        return self


class Screen(models.Model):
    id = models.AutoField(primary_key=True)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="screens")
    screen_number = models.PositiveSmallIntegerField(unique=True)
    seating_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)]
    )

    def __str__(self):
        return str(self.screen_number)


class Showing(models.Model):
    id = models.AutoField(primary_key=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="showings")
    screen = models.ForeignKey(
        Screen, on_delete=models.CASCADE, related_name="showings"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    available_seats = models.IntegerField()
    social_distancing = models.BooleanField(default=False)
    last_seat_number_assigned = models.IntegerField(default=0)
    covid_capacity = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)

    def __str__(self):
        out = self.start_time.strftime("%d %B %Y %I:%M%p")
        out = out + " - " + self.film.title
        print(out)
        return out

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + self.film.length
        super().save(*args, **kwargs)

    def archive(self):
        self.archived = True
        self.save()
        return self

    def unarchive(self):
        self.archived = False
        self.save()
        return self


class Ticket(models.Model):
    ID = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
