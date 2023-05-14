from abc import ABC
from re import search
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


# a really good habit, especially since python 3.10 is typing. https://docs.python.org/3/library/typing.html

class BaseViewSet(ABC, viewsets.ModelViewSet):
    """
        This viewset automatically provides 'list', 'create', 'retrieve',
        'update', and 'destroy' actions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements_to_capitalize_list = []
        self.model_class_name = "object"
        self.model_class = None
        self.additional_validation = False
        self.bases_of_alphabetical_order_list = []

    def get_parameters_from_request(self, request, change_first_char_case):
        request_data_dict = {}
        for item in request.query_params:
            if change_first_char_case and item in self.elements_to_capitalize_list:
                data = list(request.query_params[item].strip())
                data[0] = data[0].swapcase()
                request_data_dict[item] = "".join(data)
            else:
                request_data_dict[item] = request.query_params[item].strip()

        return request_data_dict

    def response_when_no_object_found(self, request):
        respond = f"There is no {self.model_class_name} with"
        for key, value in request.query_params.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

    def additional_validation_check(self, request_data_dict):
        return self.additional_validation, Response(
            {"Additional validation error occured."})

    # additional action functions.
    @action(detail=False, url_path="search")
    def objects_with_the_given_data(self, request, change_first_char_case=False):
        # Get parameters from URL request
        request_data_dict = self.get_parameters_from_request(request, change_first_char_case)

        # Additional validation
        validation_error, response = self.additional_validation_check(request_data_dict)
        if validation_error:
            return response

        # Filters objects with given data and respond.
        query_set = self.model_class.objects.filter(**request_data_dict)
        serializer = self.get_serializer(query_set, many=True)

        # I tried to use get_list_or_404 from django.shortcuts and it partially worked,
        # but I didn't like the way it worked - when the query_set is empty I would like
        # to use my own response_when_no_object_found function instead of
        # {
        #    "detail" = "Not found"
        #}
        if query_set:
            return Response(serializer.data)
        elif not change_first_char_case:
            return self.objects_with_the_given_data(request, change_first_char_case=True)
        else:
            return self.response_when_no_object_found(request)

    @action(detail=False, url_path="alphabetical")
    def objects_in_alphabetical_order(self, request):
        if request.query_params:
            base_of_alphabetical_order = list(request.query_params.keys())[0]
            if base_of_alphabetical_order in self.bases_of_alphabetical_order_list:
                query_set = self.model_class.objects.all().order_by(
                    base_of_alphabetical_order)
                serializer = self.get_serializer(query_set, many=True)
                return Response(serializer.data)
            else:
                return Response({"You cannot alphabetically sort by given data."})
        else:
            return Response({"Type parameter based on which you would like to sort."})


class OwnerViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements_to_capitalize_list = ["name", "surname"]
        self.model_class_name = "owner"
        self.model_class = Owner
        self.bases_of_alphabetical_order_list = ["name", "surname"]


    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class CarViewSet(BaseViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements_to_capitalize_list = ["brand", "model"]
        self.model_class_name = "car"
        self.model_class = Car
        self.additional_validation = True
        self.bases_of_alphabetical_order_list = ["brand", "model"]

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def additional_validation_check(self, request_data_dict):
        # Validate the production date variable
        if not search("[\d][\d][\d][\d][-][\d][\d][-][\d][\d]",
                      request_data_dict.get("production_date", "2000-01-01")):
            return True, Response({"Date must be in YYYY-MM-DD format."})
        return False, Response({""})

    @action(detail=False, url_path="production_date")
    def cars_in_production_date_order(self, request):
        if request.query_params:
            sort_type = list(request.query_params.keys())[0]
            if sort_type == "ascending":
                cars = Car.objects.all().order_by("production_date")
            elif sort_type == "descending":
                cars = Car.objects.all().order_by("-production_date")
            else:
                return Response({"You cannot alphabetically sort by given data."})
            serializer = self.get_serializer(cars, many=True)
            return Response(serializer.data)
        else:
            return Response({"Type '?ascending' or '?descending'."})
