import uuid
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import RouteSerializer, CitiesSerializer, SearchSerializer
from .models import Route, Cities


class ApiRoute(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['origin', 'destination']
    ordering_fields = ['departure_date', 'price']

    def get_serializer_class(self):
        if self.action == 'search':
            return SearchSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        current_time = timezone.now()
        return Route.objects.filter(
            is_seat_remaining=True
        ).exclude(
            departure_date__lt=current_time.date()
        ).exclude(
            departure_date=current_time.date(),
            departure_time__lt=current_time.time().replace(microsecond=0)
        )

    @action(detail=False, methods=["POST"])
    def search(self, request):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_time = timezone.now()
        origin = serializer.validated_data["origin"]
        destination = serializer.validated_data["destination"]
        departure_date = serializer.validated_data["departure_date"]
        no_of_passengers = serializer.validated_data["no_of_passengers"]
        routes = Route.objects.filter(
            origin=origin, destination=destination, total_seats__gte=F('tickets_sold') + no_of_passengers

        ).exclude(
            departure_date__lt=current_time.date()
        ).exclude(
            departure_date=current_time.date(),
            departure_time__lt=current_time.time().replace(microsecond=0)
        )

        route_serializer = RouteSerializer(routes, many=True)
        return Response(route_serializer.data, status=status.HTTP_200_OK)


class ApiCities(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['cities']
    permission_classes = [IsAdminOrReadOnly]

    serializer_class = CitiesSerializer
    queryset = Cities.objects.all()