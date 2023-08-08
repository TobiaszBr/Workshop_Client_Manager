import datetime
import pytest
from rest_framework import serializers
from application.models import Owner, Car
from application.serializers import OwnerSerializer, CarSerializer


@pytest.mark.django_db
@pytest.mark.parametrize(
    "owner_serializer_data",
    [{"name": "Adam", "surname": "Knafel", "phone": "123456789"}],
)
def test_owner_serializer_validate_function_valid_data(
    owner_serializer_data: dict[str, str]
) -> None:
    owner_serializer = OwnerSerializer(data=owner_serializer_data)
    assert owner_serializer.validate(owner_serializer_data) == owner_serializer_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("owner_serializer_data", "error_message"),
    [
        (
            {"name": "123", "surname": "Knafel", "phone": "123456789"},
            "Field can contain only letters and '-' without whitespaces.",
        ),
        (
            {"name": "Adam", "surname": "123", "phone": "123456789"},
            "Field can contain only letters and '-' without whitespaces.",
        ),
        (
            {"name": "Adam", "surname": "Knafel", "phone": "abc"},
            "Phone number can contain only digits",
        ),
        (
            {"name": "Adam", "surname": "Knafel", "phone": "1234"},
            "The phone number is too short - 9 digits required",
        ),
        (
            {"name": "Adam", "surname": "Knafel", "phone": "123456789123"},
            "The phone number is too long - 9 digits required",
        ),
    ],
)
def test_owner_serializer_validate_function_error_with_message(
    owner_serializer_data: dict[str, str], error_message: str
) -> None:
    with pytest.raises(serializers.ValidationError, match=error_message):
        owner_serializer = OwnerSerializer(data=owner_serializer_data)
        owner_serializer.validate(owner_serializer_data)


@pytest.mark.django_db
def test_car_serializer_validate_function_valid_data(
    valid_car_serializer_data: dict[str, str | datetime.date | Owner]
) -> None:
    car_serializer = CarSerializer(data=valid_car_serializer_data)
    assert (
        car_serializer.validate(valid_car_serializer_data) == valid_car_serializer_data
    )


@pytest.mark.django_db
def test_car_serializer_validate_function_error_with_message(
    valid_car_serializer_data: dict[str, str | datetime.date | Owner]
) -> None:
    with pytest.raises(
        serializers.ValidationError, match="Production date cannot be from the future."
    ):
        valid_car_serializer_data[
            "production_date"
        ] = datetime.date.today() + datetime.timedelta(days=1)
        car_serializer = CarSerializer(data=valid_car_serializer_data)
        car_serializer.validate(valid_car_serializer_data)
