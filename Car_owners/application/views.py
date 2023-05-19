from abc import ABC, abstractmethod
from re import search
from typing import Dict
from rest_framework import viewsets
from rest_framework.decorators import action
import rest_framework.request
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer

from django.db.models import Q

from django.db.models.fields import CharField

request_type = rest_framework.request.Request
response_type = rest_framework.response.Response


class BaseViewSet(ABC, viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.elements_to_capitalize_list = []
        self.model_class_name = "object"
        self.model_class = None
        self.additional_validation = False


    def response_when_no_object_found(self, request: request_type) -> response_type:
        respond = f"There is no {self.model_class_name} with"
        for key, value in request.query_params.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

    # additional action functions.
    @abstractmethod
    def objects_with_the_given_data(self):
        pass

    """def objects_with_the_given_data(
        self, request: request_type, change_first_char_case: bool = False
    ) -> response_type:
        # Get parameters from URL request
        request_data_dict = self.get_parameters_from_request(
            request, change_first_char_case)

        # Additional validation
        validation_error, response = self.additional_validation_check(request_data_dict)
        if validation_error:
            return response

        # Filters objects with given data and respond.
        query_set = self.model_class.objects.filter(**request_data_dict)
        serializer = self.get_serializer(query_set, many=True)

        # Return data or change first letters
        if query_set:
            return Response(serializer.data)
        elif not change_first_char_case:
            return self.objects_with_the_given_data(
                request, change_first_char_case=True                                        # tu niby to działa, ale jak zmienię np tobiasz&Bernacki to już nie (bo zawsze zmieniam oba parametry, a w sumie powinienem zmienić pojedynczo i szukać
                                                                                            # czyli w tym przypadku dla name i surname w sumie powinno szukać 4 razy?
            )
        else:
            return self.response_when_no_object_found(request)"""

    @abstractmethod
    def objects_in_alphabetical_order(self):
        pass


class OwnerViewSet(BaseViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.elements_to_capitalize_list = ["name", "surname"]
        self.model_class_name = "owner"
        self.model_class = Owner
        self.additional_validation = False

    # additional action functions.
    @action(detail=False, url_path="search")
    def objects_with_the_given_data(self, request: request_type) -> response_type:
        # Filters objects with given data and respond.
        filter_list = []

        if "name" in request.query_params.keys():
            q = Q(name__iexact = request.query_params["name"])
            filter_list.append(q)

        if "surname" in request.query_params.keys():
            q = Q(surname__iexact=request.query_params["surname"])
            filter_list.append(q)

        if "phone" in request.query_params.keys():
            q = Q(phone=request.query_params["phone"])
            filter_list.append(q)

        query_set = self.model_class.objects.filter(*filter_list)
        serializer = self.get_serializer(query_set, many=True)

        # Return data or change first letters
        if query_set:
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
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements_to_capitalize_list = ["brand", "model"]
        self.model_class_name = "car"
        self.model_class = Car
        self.additional_validation = True

    def additional_validation_check(self, request_data_dict: Dict[str, str]
    ) -> (bool, response_type):
        # Validate the production date variable
        if not search(
            "[\d][\d][\d][\d][-][\d][\d][-][\d][\d]",
            request_data_dict.get("production_date", "2000-01-01"),
        ):
            return True, Response({"Date must be in YYYY-MM-DD format."})
        return False, Response({""})

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

