import datetime
import pytest
from rest_framework.test import APIClient
from application.models import Owner, Car


@pytest.fixture
def valid_owner_data() -> Owner:
    owner_data = {"name": "Andrzej", "surname": "Starczyk", "phone": "123456789"}
    return owner_data

@pytest.fixture
def valid_owner_model_data(valid_owner_data) -> Owner:
    owner = Owner.objects.create(**valid_owner_data)
    return owner

@pytest.fixture
def valid_car_model_data(valid_owner_model_data) -> Car:
    car_data = {"brand": "Ford", "model": "Focus", "production_date": "2023-01-01", "owner": valid_owner_model_data}
    car = Car.objects.create(**car_data)
    return car

@pytest.fixture
def valid_car_serializer_data(valid_owner_model_data: Owner) -> dict[str, str | datetime.date | Owner]:
    owner = valid_owner_model_data
    return {
        "brand": "Ford",
        "model": "Focus",
        "production_date": datetime.date.today(),
        "owner": owner,
    }

@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()