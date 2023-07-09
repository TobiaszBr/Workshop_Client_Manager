import datetime
import pytest
from rest_framework import serializers
from application.models import Owner, Car
from application.serializers import OwnerSerializer, CarSerializer


def get_owner_data(n: int = 0) -> dict[str, str]:
    name = "Adam"
    surname = "Knafel"
    phone = "123456789"

    if n == 1:
        name = "123"
    elif n == 2:
        surname = "123"
    elif n == 3:
        phone = "abc"
    elif n == 4:
        phone = "1234"
    elif n == 5:
        phone = "123456789123"

    return {"name": name, "surname": surname, "phone": phone}


@pytest.fixture
def car_data() -> dict[str, str | datetime.date | Owner]:
    owner = Owner.objects.create(name="Adam", surname="Knafel", phone="123456789")
    return {
        "brand": "Ford",
        "model": "Focus",
        "production_date": datetime.date.today(),
        "owner": owner,
    }


@pytest.mark.django_db
@pytest.mark.parametrize("owner_serializer_data", [get_owner_data()])
def test_owner_serializer_validate_function_no_error(
    owner_serializer_data: dict[str, str]
) -> None:
    owner_serializer = OwnerSerializer(data=owner_serializer_data)
    assert owner_serializer.validate(owner_serializer_data) == owner_serializer_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("owner_serializer_data", "error_message"),
    [
        (
            get_owner_data(1),
            "Field can contain only letters and '-' without whitespaces.",
        ),
        (
            get_owner_data(2),
            "Field can contain only letters and '-' without whitespaces.",
        ),
        (get_owner_data(3), "Phone number can contain only digits"),
        (get_owner_data(4), "The phone number is too short - 9 digits required"),
        (get_owner_data(5), "The phone number is too long - 9 digits required"),
    ],
)
def test_owner_serializer_validate_function_error_with_message(
    owner_serializer_data: dict[str, str], error_message: str
) -> None:
    with pytest.raises(serializers.ValidationError, match=error_message):
        owner_serializer = OwnerSerializer(data=owner_serializer_data)
        owner_serializer.validate(owner_serializer_data)


@pytest.mark.django_db
def test_car_serializer_validate_function_no_error(
    car_data: dict[str, str | datetime.date | Owner]
) -> None:
    car_serializer = CarSerializer(data=car_data)
    assert car_serializer.validate(car_data) == car_data


@pytest.mark.django_db
def test_car_serializer_validate_function_error_with_message(
    car_data: dict[str, str | datetime.date | Owner]
) -> None:
    with pytest.raises(
        serializers.ValidationError, match="Production date cannot be from the future."
    ):
        car_data["production_date"] = datetime.date.today() + datetime.timedelta(days=1)
        car_serializer = CarSerializer(data=car_data)
        car_serializer.validate(car_data)
