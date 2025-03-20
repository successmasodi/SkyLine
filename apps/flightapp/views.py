import os

from django.utils import timezone
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from .payment import initiate_payment
from apps.flightapp.permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from apps.flightapp.serializers import BookingSerializer, PendingSerializer, CreatePendingSerializer, EditPendingSerializer
from .models import Route, Booking, Pending
root = os.getenv("BASE_ROUTE")


class ApiPending(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete", "options", "head"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['total_cost']

    @action(detail=True, methods=["POST"])
    def pay(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            pending = self.get_object()
            current_time = timezone.now()
            qty = pending.no_of_passengers
            flight_id = pending.flight.id
            route = Route.objects.get(id=flight_id)
            available_seats = route.total_seats - route.tickets_sold

            if available_seats >= qty:
                if route.departure_date > current_time.date() or (route.departure_date==current_time.date() and route.departure_time > current_time.time().replace(microsecond=0)):
                    user = request.user
                    pending = self.get_object()
                    amount = pending.total_cost
                    email = request.user.email
                    pending_id = str(pending.id)
                    redirect_url = f"{root}"
                    return initiate_payment(amount, email, pending_id, user)
                else:
                    data = {
                        "msg": "flight has gone. try checking for current flights",
                    }
                    return Response(data, status=HTTP_400_BAD_REQUEST)
            else:
                data = {
                    "msg": f"There are not up to {qty} seats available; only {available_seats} seats left.",
                }
                return Response(data, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def confirm_payment(self, request):
        pending_id = request.GET.get("p_id")
        pending = Pending.objects.get(id=pending_id)
        user = request.user
        flight = Route.objects.get(id=pending.flight.id)
        flight.tickets_sold += pending.no_of_passengers
        flight.check_seat_availability()
        flight.save()
        instance = Booking(flight=pending.flight, no_of_passengers=pending.no_of_passengers,
                           total_cost=pending.total_cost, owner=user, )
        instance.save()
        Pending.objects.filter(id=pending_id).delete()

        serializer = BookingSerializer(instance)

        data = {
            "msg": "payment was successful",
            "data": serializer.data
        }
        return Response(data)

    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pending.objects.all()
        return Pending.objects.filter(owner=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            qty = serializer.validated_data['no_of_passengers']
            flight_id = serializer.validated_data['flight'].id
            route = Route.objects.get(id=flight_id)
            available_seats = route.total_seats - route.tickets_sold

            if available_seats >= qty:
                instance = serializer.save(owner=request.user)
                self.perform_create(instance)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
            else:
                data = {
                    "msg": f"There are not up to {qty} seats available; only {available_seats} seats left.",
                }
                return Response(data, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PendingSerializer
        if self.request.method == 'PATCH':
            return EditPendingSerializer
        return CreatePendingSerializer


class ApiBooking(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "delete", "options", "head"]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['flight_no']
    ordering_fields = ['placed_at', 'total_cost']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
