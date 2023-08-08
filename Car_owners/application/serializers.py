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
        if search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", data.get("name", "a")):
            raise serializers.ValidationError({"name": error_text})
        elif search("[^A-Z-a-zżźćńółęąśŻŹĆĄŚĘŁÓŃ]", data.get("surname", "a")):
            raise serializers.ValidationError({"surname": error_text})
        elif search("[^0-9]", data.get("phone", "700700700")):
            raise serializers.ValidationError(
                {"phone": "Phone number can contain only digits"}
            )
        elif len(data.get("phone", "700700700")) < 9:
            raise serializers.ValidationError(
                {"phone": "The phone number is too short - 9 digits required"}
            )
        elif len(data.get("phone", "700700700")) > 9:
            raise serializers.ValidationError(
                {"phone": "The phone number is too long - 9 digits required"}
            )
        return data


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "brand", "model", "production_date", "problem_description",
                  "repaired", "total_cost", "owner"]

    def validate(self, data: collections.OrderedDict) -> collections.OrderedDict:
        """
        Checks that production date is not from the future.
        """
        if data.get("production_date", datetime.date.today()) > datetime.date.today():
            raise serializers.ValidationError(
                {"production_date": "Production date cannot be from the future."}
            )
        return data
