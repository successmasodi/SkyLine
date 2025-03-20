from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('route', views.ApiRoute, basename='route')
router.register('cities', views.ApiCities, basename='cities')


urlpatterns = [
    path("", include(router.urls)),
]

