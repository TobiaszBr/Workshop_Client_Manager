import pytest
from application.models import Owner, Car


@pytest.fixture
def valid_owner_and_car_models_data() -> dict[str, Owner | Car]:
    owner = Owner.objects.create(name="Adam", surname="Knafel", phone="123456789")
    car = Car.objects.create(
        brand="Ford", model="Focus", production_date="2023-01-01", owner=owner
    )

    return {"owner": owner, "car": car}