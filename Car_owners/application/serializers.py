from .models import Owner, Car
from rest_framework import serializers
import datetime


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['url', 'id', 'name', 'surname', 'phone']

    def validate(self, data):
        """
        Checks if name and surname contain only letters.
        """

        if not data['name'].isalpha():
            raise serializers.ValidationError(
            {'name': 'Name can contain only letters without whitespaces.'})
        elif not data['surname'].isalpha():
            raise serializers.ValidationError(
        {'surname': 'Surname can contain only letters without whitespaces.'})
        return data


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['url', 'id','brand', 'model', 'production_date', 'owner']

    def validate(self, data):
        """
        Checks that production date is not from the future.
        """
        if data['production_date'] > datetime.date.today():
            raise serializers.ValidationError(
            {'production_date': 'Production date cannot be from the future.'})
        return data