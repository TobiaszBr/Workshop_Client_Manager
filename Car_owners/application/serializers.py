import collections
import datetime
from re import search
from rest_framework import serializers
from .models import Owner, Car


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ["id", "name", "surname", "phone"]

    def validate(self, data: collections.OrderedDict) -> collections.OrderedDict:
        """
        Checks if name and surname contain only letters and '-'.
        """

        error_text = "Field can contain only letters and '-' without whitespaces."
        if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", data["name"]):
            raise serializers.ValidationError({"name": error_text})
        elif search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", data["surname"]):
            raise serializers.ValidationError({"surname": error_text})
        return data


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "brand", "model", "production_date", "owner"]

    def validate(self, data: collections.OrderedDict) -> collections.OrderedDict:
        """
        Checks that production date is not from the future.
        """
        if data["production_date"] > datetime.date.today():
            raise serializers.ValidationError(
                {"production_date": "Production date cannot be from the future."}
            )
        return data
