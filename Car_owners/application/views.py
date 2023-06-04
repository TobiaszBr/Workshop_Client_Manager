from abc import ABC, abstractmethod
import datetime
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from re import search
import rest_framework
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


request_type = rest_framework.request.Request
response_type = rest_framework.response.Response


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


class BaseViewSet(ABC, viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.filter_backends = [DjangoFilterBackend, OrderingFilter]
        self.model_class_name = ""

    @abstractmethod
    def request_validation(self, request: request_type):
        pass

    def list(self, request: request_type, *args, **kwargs) -> response_type:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Additional request validation
        validation_failed, response = self.request_validation(request)
        if validation_failed:
            return response

        # Additional custom response, when no object found
        if not serializer.data:
            return Response(f"There is no {self.model_class_name} with given data")

        return Response(serializer.data)


class OwnerViewSet(BaseViewSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.queryset = Owner.objects.all()
        self.serializer_class = OwnerSerializer
        self.filterset_class = OwnerFilter
        self.ordering_fields = ["name", "surname"]
        self.model_class_name = "Owner"

    def request_validation(self, request: request_type) -> (bool, response_type):
        for key, value in request.query_params.items():
            if key == "phone":
                if search("[^0-9]", value):
                    return True, Response({"phone": "Phone number can contain only digits"})
                elif len(value) > 9:
                    return True, Response({"phone": "Phone number is too long"})
                elif len(value) < 9:
                    return True, Response({"phone": "Phone number is too short"})
            elif key == "name" or key == "surname":
                if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", value):
                    return True, Response(
                        {
                            f"{key}": f"{key} can contain only letters and '-' without whitespaces"
                        }
                    )
            elif key == "ordering":
                if value not in self.ordering_fields:
                    ord_fields_string = ", ".join(self.ordering_fields)
                    return True, Response(
                        {
                            "ordering": f"Ordering should be one of the following: {ord_fields_string}"
                        }
                    )

        return False, Response({""})


class CarViewSet(BaseViewSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.queryset = Car.objects.all()
        self.serializer_class = CarSerializer
        self.filterset_class = CarFilter
        self.ordering_fields = ["brand", "model", "production_date"]
        self.model_class_name = "Car"

    def request_validation(self, request: request_type) -> (bool, response_type):
        for key, value in request.query_params.items():
            if key == "production_date":
                production_date_as_date_object = datetime.datetime.strptime(value, "%Y-%m-%d").date()

                if production_date_as_date_object > datetime.date.today():
                    return True, Response({"production_date": "Production date cannot be from the future."})
            elif key == "ordering":
                if value not in self.ordering_fields:
                    ord_fields_string = ", ".join(self.ordering_fields)
                    return True, Response(
                        {
                            "ordering": f"Ordering should be one of the following: {ord_fields_string}"
                        }
                    )

        return False, Response({""})
