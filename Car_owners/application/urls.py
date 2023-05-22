from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title="Car owners API",
      default_version='v1',
      description="Test description - test",
      terms_of_service="https://www.test.com/policies/terms/",
      contact=openapi.Contact(email="contact@test.local"),
      license=openapi.License(name="TEST License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"owners", views.OwnerViewSet, basename="owner")
router.register(r"cars", views.CarViewSet, basename="car")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("app/", include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
