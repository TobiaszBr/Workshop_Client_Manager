import django.utils.datastructures

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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name', 'surname', 'phone')

    @action(detail=False, url_path='search')
    def owners_with_the_given_data(self, request):

        try:
            name = request.GET['name'].title()
        except django.utils.datastructures.MultiValueDictKeyError:
            name=''

        try:
            surname = request.GET['surname'].title()
        except django.utils.datastructures.MultiValueDictKeyError:
            surname = ''

        try:
            phone = f"+{request.GET['phone'].strip()}"
        except django.utils.datastructures.MultiValueDictKeyError:
            phone = 0

        if phone:
            try:
                owners = Owner.objects.get(phone=phone)
            except Owner.DoesNotExist:
                owners = Owner.objects.filter(phone=phone)
            return check_if_queryset_is_empty(owners, 'owners', 'phone', phone,
                                          self.get_serializer, many=False)
        elif name and surname:
            owners = Owner.objects.filter(name=name, surname=surname)
            return check_if_queryset_is_empty(owners, 'owners', 'data', name,
                                              self.get_serializer, many=True)
        elif name:
            owners = Owner.objects.filter(name=name)
            return check_if_queryset_is_empty(owners, 'owners', 'name', name,
                                              self.get_serializer, many=True)
        elif surname:
            owners = Owner.objects.filter(surname=surname)
            return check_if_queryset_is_empty(owners, 'owners', 'surname', surname,
                                              self.get_serializer, many=True)



    @action(detail=False, url_path='')
    def owners_with_the_given_name(self, request):
        name = request.GET['name'].title()
        owners = Owner.objects.filter(name=name)
        return check_if_queryset_is_empty(owners, 'owners', 'name', name,
                                          self.get_serializer, many=True)

    @action(detail=False, url_path='')
    def owners_with_the_given_surname(self, request):
        surname = request.GET['surname'].title()
        owners = Owner.objects.filter(surname=surname)
        return check_if_queryset_is_empty(owners, 'owners', 'surname',
                                          surname, self.get_serializer,
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('brand', 'model')

    @action(detail=False, url_path='brand')
    def cars_with_the_given_brand(self, request):
        brand = request.GET['brand'].title()
        cars = Car.objects.filter(brand=brand)
        return check_if_queryset_is_empty(cars, 'cars', 'brand', brand,
                                          self.get_serializer, many=True)

    @action(detail=False, url_path='model')
    def cars_with_the_given_model(self, request):
        model = request.GET['model']
        cars = Car.objects.filter(model=model)
        return check_if_queryset_is_empty(cars, 'cars', 'model', model,
                                          self.get_serializer, many=True)

    @action(detail=False,
            url_path=r'(?P<brand_or_model>[brand model]+)/alphabetic')
    def cars_in_alphabetic_order(self, request, brand_or_model):
        cars = Car.objects.all().order_by(brand_or_model)
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)