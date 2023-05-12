from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer
from re import search


class OwnerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
                                                                                         # a really good habit, especially since python 3.10 is typing. https://docs.python.org/3/library/typing.html
    def get_parameters_from_request(self, request, *elements_to_capitalize_list):
        request_data_dict = {}
        for item in request.query_params:
            if item in elements_to_capitalize_list:
                request_data_dict[item] = request.query_params[item].capitalize().strip()
            else:
                request_data_dict[item] = request.query_params[item].strip()

        return request_data_dict


    def response_when_no_owner_found(self, request_data_dict):
        respond = "There is no owner with"
        for key, value in request_data_dict.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

    # additional action functions.
    @action(detail=False, url_path="search")
    def owners_with_the_given_data(self, request):
        # Get parameters from URL request
        request_data_dict = self.get_parameters_from_request(request, "name", "surname")

        # Filters owners with given data and respond.
        owners = Owner.objects.filter(**request_data_dict)
        serializer = self.get_serializer(owners, many=True)
                                                                                            # owners.exists() do zapytania czy może zostać samo owners - jaka różnica
        if owners:
            return Response(serializer.data)
        else:
            return self.response_when_no_owner_found(request_data_dict)

    @action(detail=False, url_path=r"(?P<name_or_surname>[name surname]+)/alphabetic")
    def owners_in_alphabetic_order(self, request, name_or_surname):
        owners = Owner.objects.all().order_by(name_or_surname)
        serializer = self.get_serializer(owners, many=True)
        return Response(serializer.data)


class CarViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """

    queryset = Car.objects.all()
    serializer_class = CarSerializer

    # all of my comments from OwnerViewSet also apply to this class. But you should see many repetitions of code that looks exactly the same. Make use of the fact it's OOP and use inheritance + mixins

    # To samo co w owners
    def get_parameters_from_request(self, request, *elements_to_capitalize_list):
        request_data_dict = {}
        for item in request.query_params:
            if item in elements_to_capitalize_list:
                request_data_dict[item] = request.query_params[item].capitalize().strip()
            else:
                request_data_dict[item] = request.query_params[item].strip()

        return request_data_dict

    # To samo co w owners
    def response_when_no_owner_found(self, request_data_dict):
        respond = "There is no owner with"
        for key, value in request_data_dict.items():
            respond += f" {key}: {value}"

        return Response(f"{respond}.")

    @action(detail=False, url_path="search")
    def cars_with_the_given_data(self, request):
        # Get parameters from URL request
        request_data_dict = self.get_parameters_from_request(request, "brand")


        # Data validation
        # Validate the production date variable
        if not search("[\d][\d][\d][\d][-][\d][\d][-][\d][\d]", request_data_dict.get("production_date", "2000-01-01")):
            return Response({"Date must be in YYYY-MM-DD format."})


        # Filters owners with given data and respond.
        cars = Car.objects.filter(**request_data_dict)
        serializer = self.get_serializer(cars, many=True)
        # owners.exists() do zapytania czy może zostać samo owners - jaka różnica
        if cars:
            return Response(serializer.data)
        else:
            return self.response_when_no_owner_found(request_data_dict)


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
