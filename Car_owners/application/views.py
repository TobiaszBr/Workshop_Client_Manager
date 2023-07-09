from abc import ABC, abstractmethod
import datetime
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from re import search
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .decortors import swagger_decorator_owner, swagger_decorator_car
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


request_type = Request
response_type = Response


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
        self.model_class = None
        self.model_class_name = None

    @abstractmethod
    def request_validation(self, request: request_type):
        pass

    @staticmethod
    @abstractmethod
    def get_swagger_parameters():
        pass

    def list(self, request: request_type, *args, **kwargs) -> response_type:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        # Additional request validation
        if response := self.request_validation(request):
            return response

        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Additional custom response, when no object found
        if not serializer.data:
            return Response(f"There is no {self.model_class_name} with given data")

        return Response(serializer.data)


@method_decorator(name="retrieve", decorator=swagger_decorator_owner)
@method_decorator(name="update", decorator=swagger_decorator_owner)
@method_decorator(name="partial_update", decorator=swagger_decorator_owner)
@method_decorator(name="destroy", decorator=swagger_decorator_owner)
class OwnerViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.queryset = Owner.objects.all()
        self.serializer_class = OwnerSerializer
        self.filterset_class = OwnerFilter
        self.ordering_fields = ["name", "surname"]
        self.model_class = Owner
        self.model_class_name = self.model_class._meta.object_name

    def request_validation(self, request: request_type) -> response_type:
        for key, value in request.query_params.items():
            if key == "phone":
                if search("[^0-9]", value):
                    return Response(
                        {"phone": "Phone number can contain only digits"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif len(value) > 9:
                    return Response(
                        {"phone": "Phone number is too long"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                elif len(value) < 9:
                    return Response(
                        {"phone": "Phone number is too short"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif key == "name" or key == "surname":
                if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", value):
                    return Response(
                        {
                            f"{key}": f"{key} can contain only letters and '-' without "
                            f"whitespaces"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif key == "ordering":
                if value not in self.ordering_fields:
                    ord_fields_string = ", ".join(self.ordering_fields)
                    return Response(
                        {
                            "ordering": f"Ordering should be one of the following: "
                            f"{ord_fields_string}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

    @staticmethod
    def get_swagger_parameters() -> dict[str, list[openapi.Parameter]]:
        swagger_parameters_dict = {
            "id": "Owner's unique id number",
            "name": "Owner's name",
            "surname": "Owner's surname",
            "phone": "Owner's phone number - 9 digits",
        }
        manual_parameters_list = []
        for parameter_name, description in swagger_parameters_dict.items():
            if parameter_name != "id":
                field_type = openapi.TYPE_STRING
            else:
                field_type = openapi.TYPE_INTEGER

            parameter = openapi.Parameter(
                parameter_name,
                in_=openapi.IN_QUERY,
                description=f"{description}",
                type=field_type,
            )

            manual_parameters_list.append(parameter)

        swagger_auto_schema_params_dict = {"manual_parameters": manual_parameters_list}

        return swagger_auto_schema_params_dict

    @swagger_auto_schema(**get_swagger_parameters())
    def list(self, request: request_type, *args, **kwargs) -> response_type:
        return super().list(request, *args, **kwargs)


@method_decorator(name="retrieve", decorator=swagger_decorator_car)
@method_decorator(name="update", decorator=swagger_decorator_car)
@method_decorator(name="partial_update", decorator=swagger_decorator_car)
@method_decorator(name="destroy", decorator=swagger_decorator_car)
class CarViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.queryset = Car.objects.all()
        self.serializer_class = CarSerializer
        self.filterset_class = CarFilter
        self.ordering_fields = ["brand", "model", "production_date"]
        self.model_class = Car
        self.model_class_name = self.model_class._meta.object_name

    def request_validation(self, request: request_type) -> response_type:
        for key, value in request.query_params.items():
            if key == "production_date":
                production_date_as_date_object = datetime.datetime.strptime(
                    value, "%Y-%m-%d"
                ).date()

                if production_date_as_date_object > datetime.date.today():
                    return Response(
                        {
                            "production_date": "Production date cannot be from the "
                            "future."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif key == "ordering":
                if value not in self.ordering_fields:
                    ord_fields_string = ", ".join(self.ordering_fields)
                    return Response(
                        {
                            "ordering": f"Ordering should be one of the following: "
                            f"{ord_fields_string}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

    @staticmethod
    def get_swagger_parameters() -> dict[str, list[openapi.Parameter]]:
        swagger_parameters_dict = {
            "id": "Car's unique id number",
            "brand": "Car's brand",
            "model": "Car's model",
            "production_date": "Car's production date in YYYY-MM-DD format",
            "owner": "Car owner's unique id number",
        }
        manual_parameters_list = []
        for parameter_name, description in swagger_parameters_dict.items():
            if parameter_name not in ["id", "owner"]:
                field_type = openapi.TYPE_STRING
            else:
                field_type = openapi.TYPE_INTEGER

            parameter = openapi.Parameter(
                parameter_name,
                in_=openapi.IN_QUERY,
                description=f"{description}",
                type=field_type,
            )

            manual_parameters_list.append(parameter)

        swagger_auto_schema_params_dict = {"manual_parameters": manual_parameters_list}

        return swagger_auto_schema_params_dict

    @swagger_auto_schema(**get_swagger_parameters())
    def list(self, request: request_type, *args, **kwargs) -> response_type:
        return super().list(request, *args, **kwargs)
