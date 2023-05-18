from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"owners", views.OwnerViewSet, basename="owner")
router.register(r"cars", views.CarViewSet, basename="car")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
