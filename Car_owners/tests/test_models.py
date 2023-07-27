import pytest
from application.models import Owner, Car


@pytest.mark.django_db
def test_owner_display_str_method(
    valid_owner_and_car_models_data: dict[str, Owner | Car]
) -> None:
    assert (
        str(valid_owner_and_car_models_data["owner"])
        == f"{valid_owner_and_car_models_data['owner'].name} {valid_owner_and_car_models_data['owner'].surname}"
    )


@pytest.mark.django_db
def test_car_display_str_method(
    valid_owner_and_car_models_data: dict[str, Owner | Car]
) -> None:
    assert (
        str(valid_owner_and_car_models_data["car"])
        == f"{valid_owner_and_car_models_data['car'].brand} {valid_owner_and_car_models_data['car'].model}"
    )
