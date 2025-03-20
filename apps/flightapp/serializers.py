from rest_framework.fields import SerializerMethodField

from .models import Pending, Booking
from rest_framework import serializers

from ..route.serializers import RouteViewSerializer


class PendingSerializer(serializers.ModelSerializer):
    flight = RouteViewSerializer(read_only=True)

    class Meta:
        model = Pending
        fields = ['id', 'flight', 'no_of_passengers', 'total_cost']
        read_only_fields = ['total_cost', ]


class CreatePendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pending
        fields = ['id', 'flight', 'no_of_passengers', 'total_cost']
        read_only_fields = ['total_cost', ]


class EditPendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pending
        fields = ['flight', 'no_of_passengers']


class BookingSerializer(serializers.ModelSerializer):
    flight = RouteViewSerializer(read_only=True)
    passenger_name = SerializerMethodField(method_name='get_passenger_name')

    class Meta:
        model = Booking
        fields = ['owner', 'passenger_name', 'flight_no', 'flight', 'no_of_passengers', 'check_in', 'total_cost',
                  'placed_at']
        read_only_fields = ['owner', 'total_cost']

    def get_passenger_name(self, obj):
        owner = obj.owner
        return f"{owner.first_name} {owner.last_name}"




