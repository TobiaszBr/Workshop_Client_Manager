import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from re import search
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import Owner, Car
from .serializers import OwnerSerializer, CarSerializer


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


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OwnerFilter
    ordering_fields = ["name", "surname"]


    def request_validation(self, request):                                                  # hintsy
        for key, value in request.query_params.items():
            if key == "phone":
                if search("[^0-9]", value):
                    return True, Response({"phone": "Phone number can contain only digits"})
                elif len(value) > 9:
                    return True, Response({"phone": "Phone number is too long"})
                elif len(value) < 9:
                    return True, Response({"phone": "Phone number is too short"})
            elif key == "name" or key == "surname":
                if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", value):
                    return True, Response(
                        {
                            f"{key}": f"{key} can contain only letters and '-' without whitespaces"
                        }
                    )
            elif key == "ordering":
                if value not in ["name", "surname"]:
                    ord_fields_string = ", ".join(["name", "surname"])
                    return True, Response(
                        {
                            "ordering": f"Ordering should be one of the following: {ord_fields_string}"
                        }
                    )

        return False, Response({""})                                                # hintsy

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        # Additional request validation
        validation_failed, response = self.request_validation(request)
        if validation_failed:
            return response

        # Additional custom response, when no object found
        if not serializer.data:
            return Response("There is no owner with given data")

        return Response(serializer.data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CarFilter
    ordering_fields = ["brand", "model", "production_date"]
