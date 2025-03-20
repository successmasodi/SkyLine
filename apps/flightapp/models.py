from datetime import datetime, date

from django.conf import settings
from django.db import models
import uuid
from django.utils import timezone
from apps.route.models import Route


class Pending(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    flight = models.ForeignKey(Route, on_delete=models.CASCADE)
    no_of_passengers = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_cost = self.flight.price * self.no_of_passengers
        super().save(*args, **kwargs)


class Booking(models.Model):
    flight_no = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    flight = models.ForeignKey(Route, on_delete=models.CASCADE)
    no_of_passengers = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    check_in = models.BooleanField(default=False)

    def is_flight_in_past(self):
        departure_date = self.flight.departure_date
        departure_time = self.flight.departure_time
        departure_datetime = datetime.combine(departure_date, departure_time)
        departure_datetime = timezone.make_aware(departure_datetime, timezone.get_default_timezone())
        return departure_datetime < timezone.now()
