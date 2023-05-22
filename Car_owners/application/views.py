from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
import rest_framework.request
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


request_type = rest_framework.request.Request
response_type = rest_framework.response.Response


class BaseViewSet(ABC, viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.model_class = None
        self.model_class_name = "object"

    def response_when_no_object_found(self, request: request_type) -> response_type:
        respond = f"There is no {self.model_class_name} with"
        for key, value in request.query_params.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

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

    # additional action functions.
    @action(detail=False, url_path="search")
    def objects_with_the_given_data(self, request: request_type) -> response_type:
        # Filters objects with given data and respond.
        filter_list = []

        if "name" in request.query_params.keys():                                           # postaraj się zrobić to bardziej uniwersalnie?
            q = Q(name__iexact = request.query_params["name"])
            filter_list.append(q)

        if "surname" in request.query_params.keys():
            q = Q(surname__iexact=request.query_params["surname"])
            filter_list.append(q)

        if "phone" in request.query_params.keys():
            q = Q(phone=request.query_params["phone"])
            filter_list.append(q)

        queryset = self.queryset.filter(*filter_list)
        serializer = self.get_serializer(queryset, many=True)

        # Return data or change first letters
        if queryset:
            return Response(serializer.data)
        else:
            return self.response_when_no_object_found(request)

    @action(detail=False, url_path=r"alphabetical/(?P<alphabetical_base>[name surname]+)")
    def objects_in_alphabetical_order(self, request: request_type, alphabetical_base: str
    ) -> response_type:

        query_set = self.model_class.objects.all().order_by(alphabetical_base)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)


class CarViewSet(BaseViewSet):
    
    serializer_class = CarSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_class = Car
        self.model_class_name = self.model_class._meta.object_name
        self.queryset = self.model_class.objects.all()

    def additional_validation_check(self, request_data_dict: Dict[str, str]
    ) -> (bool, response_type):
        # Validate the production date variable
        date_string = request_data_dict.get("production_date", "2000-01-01")
        try:
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
            print(date_object)
        except ValueError:
            return True, Response({"Date out of range or wrong date format - must be YYYY-MM-DD."})

        return False, Response({""})


    # additional action functions.
    @action(detail=False, url_path="search")
    def objects_with_the_given_data(self, request: request_type) -> response_type:
        # Additional validation
        validation_error, response = self.additional_validation_check(request.query_params)
        if validation_error:
            return response

        # Filters objects with given data and respond.
        filter_list = []
        if "brand" in request.query_params.keys():
            q = Q(brand__iexact=request.query_params["brand"])
            filter_list.append(q)
        if "model" in request.query_params.keys():
            q = Q(model__iexact=request.query_params["model"])
            filter_list.append(q)
        if "production_date" in request.query_params.keys():
            q = Q(production_date=request.query_params["production_date"])
            filter_list.append(q)
        if "owner" in request.query_params.keys():
            q = Q(owner=request.query_params["owner"])
            filter_list.append(q)

        queryset = self.queryset.filter(*filter_list)
        serializer = self.get_serializer(queryset, many=True)

        # Return data or change first letters
        if queryset:
            return Response(serializer.data)
        else:
            return self.response_when_no_object_found(request)

    @action(detail=False, url_path=r"production_date/(?P<sort_order>[ascending descending]+)")
    def cars_in_production_date_order(self, request: request_type, sort_order: str) -> response_type:
        if sort_order == "ascending":
            query_set = self.model_class.objects.all().order_by("production_date")
        elif sort_order == "descending":
            query_set = self.model_class.objects.all().order_by("-production_date")
        else:
            return Response({"Wrong url."})

        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path=r"alphabetical/(?P<alphabetical_base>[brand model]+)")
    def objects_in_alphabetical_order(self, request: request_type, alphabetical_base: str) -> response_type:
        query_set = self.model_class.objects.all().order_by(alphabetical_base)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)
