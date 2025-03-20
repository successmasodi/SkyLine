from rest_framework.fields import SerializerMethodField

from .models import Route, Cities
from rest_framework import serializers


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    no_of_passengers = serializers.IntegerField(default=1)

    class Meta:
        model = Route
        fields = ['origin', 'destination', 'departure_date','no_of_passengers' ]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'
        read_only_fields = ['tickets_sold', 'is_seat_remaining']


class RouteViewSerializer(serializers.ModelSerializer):
    origin = CitiesSerializer(read_only=True)
    destination = CitiesSerializer(read_only=True)

    class Meta:
        model = Route
        fields = ['departure_date', 'departure_time', 'origin', 'destination', 'price']





