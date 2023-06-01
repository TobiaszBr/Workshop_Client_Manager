from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List

from django.db.models import Q, query_utils
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from rest_framework.decorators import action
import rest_framework.request
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer

import django_filters

request_type = rest_framework.request.Request
response_type = rest_framework.response.Response
q_type = query_utils.Q


class BaseViewSet(ABC, viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.model_class = None
        self.model_class_name = "object"
        self.queryset = None
        self.case_insensitive_fields = []

    def response_when_no_object_found(self, request: request_type) -> response_type:
        respond = f"There is no {self.model_class_name} with"
        for key, value in request.query_params.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

    def get_filter_list(self, request: request_type) -> List[q_type]:
        filter_list = []
        model_fields_names_list = [
            element.name for element in self.model_class._meta.get_fields()
        ]

        for field in model_fields_names_list:
            if field in request.query_params.keys():
                parameters_dict = {}
                if field in self.case_insensitive_fields:
                    parameters_dict[f"{field}__iexact"] = request.query_params[field]
                else:
                    parameters_dict[field] = request.query_params[field]

                q = Q(**parameters_dict)
                filter_list.append(q)

        return filter_list

    @abstractmethod
    def additional_validation_check(self):
        pass

    # additional action functions.
    @abstractmethod
    def objects_with_the_given_data(self):
        pass

    @abstractmethod
    def objects_in_alphabetical_order(self):
        pass


class OwnerViewSet(BaseViewSet):
    serializer_class = OwnerSerializer

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.model_class = Owner
        self.model_class_name = self.model_class._meta.object_name
        self.queryset = self.model_class.objects.all()
        self.case_insensitive_fields = ["name", "surname"]

    def additional_validation_check(
        self, request_data_dict: Dict[str, str]
    ) -> (bool, response_type):
        phone_number = request_data_dict.get("phone", "000000000")
        if len(phone_number) < 9:
            return True, Response({"Phone number is to short."})
        elif len(phone_number) > 9:
            return True, Response({"Phone number is to long."})
        else:
            return False, Response({""})

    @staticmethod
    def get_swagger_search_parameters():
        swagger_search_parameters_dict = {
            "id": "Owner's unique id number",
            "name": "Owner's name",
            "surname": "Owner's surname",
            "phone": "Owner's phone number - 9 digits",
        }
        manual_parameters_list = []
        for parameter_name, description in swagger_search_parameters_dict.items():
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

    # additional action functions.
    @swagger_auto_schema(**get_swagger_search_parameters())
    @action(detail=False, url_path="search")
    def objects_with_the_given_data(self, request: request_type) -> response_type:
        # Additional validation
        validation_error, response = self.additional_validation_check(
            request.query_params
        )
        if validation_error:
            return response

        filter_list = self.get_filter_list(request)
        queryset = self.queryset.filter(*filter_list)
        serializer = self.get_serializer(queryset, many=True)

        # Return data or change first letters
        if queryset:
            return Response(serializer.data)
        else:
            return self.response_when_no_object_found(request)

    @action(
        detail=False, url_path=r"alphabetical/(?P<alphabetical_base>[name surname]+)"
    )
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "alphabetical_base",
                in_=openapi.IN_PATH,
                description="Select base of alphabetical order: name or surname",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def objects_in_alphabetical_order(
        self, request: request_type, alphabetical_base: str
    ) -> response_type:
        query_set = self.queryset.all().order_by(alphabetical_base)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)


class CarViewSet(BaseViewSet):
    serializer_class = CarSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = Car
        self.model_class_name = self.model_class._meta.object_name
        self.queryset = self.model_class.objects.all()
        self.case_insensitive_fields = ["brand", "model"]

    def additional_validation_check(
        self, request_data_dict: Dict[str, str]
    ) -> (bool, response_type):
        # Validate the production date variable
        date_string = request_data_dict.get("production_date", "2000-01-01")
        try:
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            return True, Response(
                {"Date out of range or wrong date format - must be YYYY-MM-DD."}
            )

        return False, Response({""})

    @staticmethod
    def get_swagger_search_parameters():
        swagger_search_parameters_dict = {
            "id": "Car's unique id number",
            "brand": "Car's brand",
            "model": "Car's model",
            "production_date": "Car's production date in YYYY-MM-DD format",
            "owner": "Car owner's id",
        }

        manual_parameters_list = []
        for parameter_name, description in swagger_search_parameters_dict.items():
            if parameter_name in ["id", "owner"]:
                field_type = openapi.TYPE_INTEGER
            elif parameter_name == "production_date":
                field_type = openapi.FORMAT_DATE
            else:
                field_type = openapi.TYPE_STRING

            parameter = openapi.Parameter(
                parameter_name,
                in_=openapi.IN_QUERY,
                description=f"{description}",
                type=field_type,
            )

            manual_parameters_list.append(parameter)

        swagger_auto_schema_params_dict = {"manual_parameters": manual_parameters_list}

        return swagger_auto_schema_params_dict

    # additional action functions.
    @swagger_auto_schema(**get_swagger_search_parameters())
    @action(detail=False, url_path="search")
    def objects_with_the_given_data(self, request: request_type) -> response_type:
        # Additional validation
        validation_error, response = self.additional_validation_check(
            request.query_params
        )
        if validation_error:
            return response

        filter_list = self.get_filter_list(request)
        queryset = self.queryset.filter(*filter_list)
        serializer = self.get_serializer(queryset, many=True)

        # Return data or change first letters
        if queryset:
            return Response(serializer.data)
        else:
            return self.response_when_no_object_found(request)

    @action(
        detail=False,
        url_path=r"production_date/(?P<sort_order>[ascending descending]+)",
    )
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "sort_order",
                in_=openapi.IN_PATH,
                description="Select cars' production date order: ascending or descending",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def cars_in_production_date_order(
        self, request: request_type, sort_order: str
    ) -> response_type:
        if sort_order == "ascending":
            query_set = self.queryset.all().order_by("production_date")
        elif sort_order == "descending":
            query_set = self.queryset.all().order_by("-production_date")
        else:
            return Response({"Wrong url."})

        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)

    @action(
        detail=False, url_path=r"alphabetical/(?P<alphabetical_base>[brand model]+)"
    )
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "alphabetical_base",
                in_=openapi.IN_PATH,
                description="Select base of alphabetical order: brand or model",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def objects_in_alphabetical_order(
        self, request: request_type, alphabetical_base: str
    ) -> response_type:
        query_set = self.queryset.all().order_by(alphabetical_base)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)


class TestFilterOwner(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    surname = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Owner
        fields = ["id", "name", "surname", "phone"]


class TestViewSetOwner(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TestFilterOwner




class TestFilterCar(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr='iexact')
    model = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Car
        fields = ["id", "brand", "model", "production_date", "owner"]


class TestViewSetCar(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TestFilterCar