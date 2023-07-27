import pytest
from application.models import Owner, Car


@pytest.mark.django_db
def test_owner_display_str_method(valid_owner_model_data: Owner) -> None:
    assert (
        str(valid_owner_model_data)
        == f"{valid_owner_model_data.name} {valid_owner_model_data.surname}"
    )


@pytest.mark.django_db
def test_car_display_str_method(valid_car_model_data: Car) -> None:
    assert (
        str(valid_car_model_data)
        == f"{valid_car_model_data.brand} {valid_car_model_data.model}"
    )
