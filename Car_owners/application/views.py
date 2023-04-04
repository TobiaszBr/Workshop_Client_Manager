from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters import rest_framework as filters


def check_if_queryset_is_empty(queryset, objects, parameter_to_check,
        parameter_to_check_input, serializer, many=False):
    if queryset:
        serializer = serializer(queryset, many=many)
        return Response(serializer.data)
    return Response(f"There are no {objects} with {parameter_to_check}"
                    f" {parameter_to_check_input}")


class OwnerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions.
    """

    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    @action(detail=False, url_path=r'name/(?P<name>\w+)')
    def owners_with_the_given_name(self, request, name):
        owners = Owner.objects.filter(name=name.title())
        return check_if_queryset_is_empty(owners, 'owners', 'name',
                                          name.title(),
                                          self.get_serializer, many=True)

    @action(detail=False, url_path=r'surname/(?P<surname>\w+)')
    def owners_with_the_given_surname(self, request, surname):
        owners = Owner.objects.filter(surname=surname.title())
        return check_if_queryset_is_empty(owners, 'owners', 'surname',
                                          surname.title(), self.get_serializer,
                                          many=True)

    @action(detail=False,
            url_path=r'(?P<name_or_surname>[name surname]+)/alphabetic')
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

    @action(detail=False, url_path=r'brand/(?P<brand>\w+)')
    def cars_with_the_given_brand(self, request, brand):
        cars = Car.objects.filter(brand=brand)
        return check_if_queryset_is_empty(cars, 'cars', 'brand', brand,
                                          self.get_serializer, many=True)

    # To further debugging
    @action(detail=False, url_path=r'model/(?P<model>\w+)')
    def cars_with_the_given_model(self, request, model):
        cars = Car.objects.filter(model=model)
        return check_if_queryset_is_empty(cars, 'cars', 'model', model,
                                          self.get_serializer, many=True)

    @action(detail=False,
            url_path=r'(?P<brand_or_model>[brand model]+)/alphabetic')
    def cars_in_alphabetic_order(self, request, brand_or_model):
        cars = Car.objects.all().order_by(brand_or_model)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)


    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('brand',)

    @action(detail=False,
            url_path='test')
    def test_function(self, request):
        cars = Car.objects.filter(brand=request.GET['brand'])
        serializer = self.get_serializer(cars, many=True)
        print(request.GET['brand'])
        return Response(serializer.data)