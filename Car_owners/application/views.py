from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer
from re import search

# a really good habit, especially since python 3.10 is typing. https://docs.python.org/3/library/typing.html

class BaseViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides 'list', 'create', 'retrieve',
        'update', and 'destroy' actions.
    """

    elements_to_capitalize_list = []
    model_class_name = "object"
    model_class = Owner
    additional_validation = False

    def get_parameters_from_request(self, request):
        request_data_dict = {}
        for item in request.query_params:
            if item in self.elements_to_capitalize_list:
                request_data_dict[item] = request.query_params[item].capitalize().strip()
            else:
                request_data_dict[item] = request.query_params[item].strip()

        return request_data_dict

    def response_when_no_object_found(self, request_data_dict):
        respond = f"There is no {self.model_class_name} with"
        for key, value in request_data_dict.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

    def additional_validation_check(self, request_data_dict):
        return self.additional_validation, Response(
            {"Additional validation error occured."})

    # additional action functions.
    @action(detail=False, url_path="search")
    def object_with_the_given_data(self, request):
        # Get parameters from URL request
        request_data_dict = self.get_parameters_from_request(request)

        # Additional validation
        validation_error, response = self.additional_validation_check(request_data_dict)
        if validation_error:
            return response

        # Filters objects with given data and respond.
        query_set = self.model_class.objects.filter(**request_data_dict)
        serializer = self.get_serializer(query_set, many=True)
                                                                                            # objects.exists() do zapytania czy może zostać samo owners - jaka różnica
        if query_set:
            return Response(serializer.data)
        else:
            return self.response_when_no_object_found(request_data_dict)


class OwnerViewSet(BaseViewSet):

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    elements_to_capitalize_list = ["name", "surname"]
    model_class_name = "owner"
    model_class = Owner

    @action(detail=False, url_path=r"(?P<name_or_surname>[name surname]+)/alphabetic")
    def owners_in_alphabetic_order(self, request, name_or_surname):
        owners = Owner.objects.all().order_by(name_or_surname)
        serializer = self.get_serializer(owners, many=True)
        return Response(serializer.data)


class CarViewSet(BaseViewSet):

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    elements_to_capitalize_list = ["brand"]
    model_class_name = "car"
    model_class = Car
    additional_validation = True

    def additional_validation_check(self, request_data_dict):
        # Validate the production date variable
        if not search("[\d][\d][\d][\d][-][\d][\d][-][\d][\d]",
                      request_data_dict.get("production_date", "2000-01-01")):
            return True, Response({"Date must be in YYYY-MM-DD format."})
        return False, Response({""})



    @action(detail=False, url_path=r"(?P<brand_or_model>[brand model]+)/alphabetic")
    def cars_in_alphabetic_order(self, request, brand_or_model):
        cars = Car.objects.all().order_by(brand_or_model)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        url_path=r"production_date/"
        r"(?P<ascending_or_descending>[ascending descending]+)",
    )
    def cars_in_production_date_order(self, request, ascending_or_descending):
        if ascending_or_descending == "ascending":
            cars = Car.objects.all().order_by("production_date")
        elif ascending_or_descending == "descending":
            cars = Car.objects.all().order_by("-production_date")

        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)
