import pytest
from application.models import Owner, Car


@pytest.fixture
def model_data() -> dict[str, Owner | Car]:
    owner = Owner.objects.create(name="Adam", surname="Knafel", phone="123456789")
    car = Car.objects.create(
        brand="Ford", model="Focus", production_date="2023-01-01", owner=owner
    )

    return {"owner": owner, "car": car}


@pytest.mark.django_db
def test_owner_display_str_method(model_data: dict[str, Owner | Car]) -> None:
    assert (
        model_data["owner"].__str__()
        == f"{model_data['owner'].name} {model_data['owner'].surname}"
    )


@pytest.mark.django_db
def test_car_display_str_method(model_data: dict[str, Owner | Car]) -> None:
    assert (
        model_data["car"].__str__()
        == f"{model_data['car'].brand} {model_data['car'].model}"
    )
