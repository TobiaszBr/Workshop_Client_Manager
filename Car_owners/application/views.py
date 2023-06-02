import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


class OwnerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    surname = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Owner
        fields = ["id", "name", "surname", "phone"]


class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr='iexact')
    model = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Car
        fields = ["id", "brand", "model", "production_date", "owner"]


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OwnerFilter
    ordering_fields = ["name", "surname"]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CarFilter
    ordering_fields = ["brand", "model", "production_date"]
