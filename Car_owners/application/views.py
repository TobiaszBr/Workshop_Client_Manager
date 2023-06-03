import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from re import search
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


class OwnerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="iexact")
    surname = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Owner
        fields = ["id", "name", "surname", "phone"]


class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr="iexact")
    model = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Car
        fields = ["id", "brand", "model", "production_date", "owner"]


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OwnerFilter
    ordering_fields = ["name", "surname"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        if (phone := request.query_params.get("phone", "123456789")) != "123456789":
            if search("[^0-9]", phone):
                return Response({"phone": "Phone number can contain only digits"})
            elif len(phone) > 9:
                return Response({"phone": "Phone number is too long"})
            elif len(phone) < 9:
                return Response({"phone": "Phone number is too short"})

        if (name := request.query_params.get("name", "dummy")) != "dummy":
            if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", name):
                return Response(
                    {
                        "name": "Name can contain only letters and '-' without whitespaces"
                    }
                )

        if (surname := request.query_params.get("surname", "dummy")) != "dummy":
            if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", surname):
                return Response(
                    {
                        "surname": "surname can contain only letters and '-' without whitespaces"
                    }
                )

        if (ordering := request.query_params.get("ordering", "dummy")) != "dummy":
            if ordering not in ["name", "surname"]:
                ord_fields_string = ", ".join(["name", "surname"])
                return Response(
                    {
                        "ordering": f"Ordering should be one of the following: {ord_fields_string}"
                    }
                )

        if not serializer.data:
            return Response("There is no owner with given data")

        return Response(serializer.data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CarFilter
    ordering_fields = ["brand", "model", "production_date"]
