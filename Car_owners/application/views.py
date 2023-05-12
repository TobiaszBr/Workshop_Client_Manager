from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer




class OwnerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_parameters_from_request(self, request):
        request_data_dict = {}
        for item in request.query_params:
            if item == "name" or item == "surname":
                request_data_dict[item] = request.query_params[item].capitalize().strip()
            else:
                request_data_dict[item] = request.query_params[item].strip()

        return request_data_dict

    def owner_parameters_search_logic(self, request_data_dict): # a really good habit, especially since python 3.10 is typing. https://docs.python.org/3/library/typing.html

        owners = Owner.objects.filter(**request_data_dict)
        serializer = self.get_serializer(owners, many=True)
        # owners.exists() do zapytania czy może zostać samo owners - jaka różnica
        if owners:
            return Response(serializer.data)
        else:
            return Response("There is no owner with given data.")



    # additional action functions.
    @action(detail=False, url_path="search")
    def owners_with_the_given_data(self, request):
        # Get parameters from URL request
        request_data_dict = self.get_parameters_from_request(request)

        # Owner's parameters search and filter logic with responds.
        return self.owner_parameters_search_logic(request_data_dict)




    # To zostaje
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

    def get_parameters_from_request(self, request): # all of my comments from OwnerViewSet also apply to this class. But you should see many repetitions of code that looks exactly the same. Make use of the fact it's OOP and use inheritance + mixins
        try:
            brand = request.GET["brand"].title()
        except MultiValueDictKeyError:
            brand = ""
        try:
            model = request.GET["model"].title()
        except MultiValueDictKeyError:
            model = ""
        try:
            production_date = request.GET["production_date"]
        except MultiValueDictKeyError:
            production_date = 0
        try:
            owner = request.GET["owner_id"] # name the variable owner_id then
        except MultiValueDictKeyError:
            owner = ""

        return brand, model, production_date, owner

    def car_parameters_search_logic(self, brand, model, production_date, owner):
        # Validate the production date variable
        if production_date:
            try:
                Car.objects.filter(production_date=production_date)
            except ValidationError as error:
                return Response({error.messages[0]})

        # Validate the owner variable
        if owner:
            try:
                Car.objects.filter(owner=int(owner))
            except ValueError:
                return Response({"Owner id must be a number."}) # line 156 says otherwise ;)

        if brand and model and production_date:
            cars = Car.objects.filter(
                brand=brand, model=model, production_date=production_date
            )
            return check_if_queryset_is_empty(
                cars,
                "car",
                "brand, model and production date",
                self.get_serializer,
                *[brand, model, production_date],
                many=True,
            )

        elif brand and model:
            cars = Car.objects.filter(brand=brand, model=model)
            return check_if_queryset_is_empty(
                cars,
                "car",
                "brand and model",
                self.get_serializer,
                *[brand, model],
                many=True,
            )

        elif brand and production_date:
            cars = Car.objects.filter(brand=brand, production_date=production_date)
            return check_if_queryset_is_empty(
                cars,
                "car",
                "brand and production date",
                self.get_serializer,
                *[brand, production_date],
                many=True,
            )

        elif model and production_date:
            cars = Car.objects.filter(model=model, production_date=production_date)
            return check_if_queryset_is_empty(
                cars,
                "car",
                "model and production date",
                self.get_serializer,
                *[model, production_date],
                many=True,
            )

        elif brand:
            cars = Car.objects.filter(brand=brand)
            return check_if_queryset_is_empty(
                cars, "car", "brand", self.get_serializer, brand, many=True
            )

        elif model:
            cars = Car.objects.filter(model=model)
            return check_if_queryset_is_empty(
                cars, "car", "model", self.get_serializer, model, many=True
            )

        elif production_date:
            cars = Car.objects.filter(production_date=production_date)
            return check_if_queryset_is_empty(
                cars,
                "car",
                "production date",
                self.get_serializer,
                production_date,
                many=True,
            )

        elif owner:
            cars = Car.objects.filter(owner=int(owner))
            return check_if_queryset_is_empty(
                cars, "car", "owner id", self.get_serializer, owner, many=True
            )

        else:
            return Response({"You did not put any parameter to search " "function."})

    @action(detail=False, url_path="search")
    def cars_with_the_given_data(self, request):
        # Try to get parameters from URL request
        brand, model, production_date, owner = self.get_parameters_from_request(request)

        # Car's parameters search and filter logic with responds.
        return self.car_parameters_search_logic(brand, model, production_date, owner)

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
