from django.urls import path, include


urlpatterns = [
    path('', include('apps.flightapp.urls')),
    path('', include('apps.route.urls')),
]
