from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('pending', views.ApiPending, basename='pending')
router.register('booking', views.ApiBooking, basename='booking')


urlpatterns = [
    path("", include(router.urls)),
]

