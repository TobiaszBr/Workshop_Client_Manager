import datetime
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from application.models import Owner, Car
from application.views import OwnerViewSet, CarViewSet


@pytest.mark.django_db
def test_create_owner(
    api_client: APIClient, valid_owner_data: dict[str, str]
) -> None:
    # create owner
    response_create_owner = api_client.post(
        "/app/owners/", data=valid_owner_data, format="json"
    )
    assert response_create_owner.status_code == status.HTTP_201_CREATED
    assert all(
        [
            response_create_owner.data[key] == valid_owner_data[key]
            for key in valid_owner_data.keys()
        ]
    )


@pytest.mark.django_db
def test_get_owner(
    api_client: APIClient, valid_owner_model_data: Owner
) -> None:
    owner_id = valid_owner_model_data.id
    # get owner
    response_get_owner = api_client.get(f"/app/owners/{owner_id}/", format="json")
    valid_owner_model_data_dict = vars(valid_owner_model_data)
    del valid_owner_model_data_dict["_state"]
    assert response_get_owner.status_code == status.HTTP_200_OK
    assert all(
        [response_get_owner.data[key] == vars(valid_owner_model_data)[key] for key in valid_owner_model_data_dict.keys()]
    )


@pytest.mark.django_db
def test_patch_owner(api_client: APIClient, valid_owner_model_data: Owner, valid_new_owner_data: dict[str, str]) -> None:
    # update owner
    owner_id = valid_owner_model_data.id
    response_patch_owner = api_client.patch(
        f"/app/owners/{owner_id}/", data=valid_new_owner_data, format="json"
    )
    assert response_patch_owner.status_code == status.HTTP_200_OK
    assert all(
        [response_patch_owner.data[key] == valid_new_owner_data[key] for key in valid_new_owner_data.keys()]
    )

    # owner does not exist
    response_patch_owner = api_client.patch(
        f"/app/owners/{owner_id + 1}/", data=valid_new_owner_data, format="json"
    )
    assert response_patch_owner.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_owner(api_client: APIClient, valid_owner_model_data: Owner) -> None:
    # delete owner
    owner_id = valid_owner_model_data.id
    response_delete_owner = api_client.delete(f"/app/owners/{owner_id}/", format="json")
    assert response_delete_owner.status_code == status.HTTP_204_NO_CONTENT

    # try to get that owner
    response_get_owner = api_client.get(f"/app/owners/{owner_id}/", format="json")
    assert response_get_owner.status_code == status.HTTP_404_NOT_FOUND

    # Owner does not exist
    response_delete_owner = api_client.delete(
        f"/app/owners/{owner_id + 1}/", format="json"
    )
    assert response_delete_owner.status_code == status.HTTP_404_NOT_FOUND







# CAR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@pytest.mark.django_db
def test_create_and_get_car(
    api_client: APIClient, valid_car_view_data: dict[str, str | int]
) -> None:
    # create car
    response_create_car = api_client.post("/app/cars/", data=valid_car_view_data, format="json")
    car_id = response_create_car.data["id"]
    assert response_create_car.status_code == status.HTTP_201_CREATED
    assert all(
        [response_create_car.data[key] == valid_car_view_data[key] for key in valid_car_view_data.keys()]
    )

    # get car
    response_get_car = api_client.get(f"/app/cars/{car_id}/", format="json")
    assert response_get_car.status_code == status.HTTP_200_OK
    assert all([response_get_car.data[key] == valid_car_view_data[key] for key in valid_car_view_data.keys()])


@pytest.mark.django_db
def test_patch_car(api_client: APIClient, valid_car_view_data: dict[str, str | int]) -> None:
    # create car
    response_create_car = api_client.post("/app/cars/", data=valid_car_view_data, format="json")
    car_id = response_create_car.data["id"]
    assert response_create_car.status_code == status.HTTP_201_CREATED
    assert all(
        [response_create_car.data[key] == valid_car_view_data[key] for key in valid_car_view_data.keys()]
    )

    # update car
    valid_car_view_data["production_date"] = "2023-06-10"
    response_patch_car = api_client.patch(
        f"/app/cars/{car_id}/", data=valid_car_view_data, format="json"
    )
    assert response_patch_car.status_code == status.HTTP_200_OK
    assert response_patch_car.data["production_date"] == valid_car_view_data["production_date"]

    # car does not exist
    response_patch_car = api_client.patch(
        f"/app/cars/{car_id + 1}/", data=valid_car_view_data, format="json"
    )
    assert response_patch_car.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_car(api_client: APIClient, valid_car_view_data: dict[str, str | int]) -> None:
    # create car
    response_create_car = api_client.post("/app/cars/", data=valid_car_view_data, format="json")
    car_id = response_create_car.data["id"]
    assert response_create_car.status_code == status.HTTP_201_CREATED
    assert all(
        [response_create_car.data[key] == valid_car_view_data[key] for key in valid_car_view_data.keys()]
    )

    # delete car
    response_delete_car = api_client.delete(f"/app/cars/{car_id}/", format="json")
    assert response_delete_car.status_code == status.HTTP_204_NO_CONTENT

    # try to get that car
    response_get_car = api_client.get(f"/app/cars/{car_id}/", format="json")
    assert response_get_car.status_code == status.HTTP_404_NOT_FOUND

    # Car does not exist
    response_delete_car = api_client.delete(f"/app/cars/{car_id + 1}/", format="json")
    assert response_delete_car.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    ("data", "expected_message"),
    [
        ({"phone": "asd1234cvb"}, "Phone number can contain only digits"),
        ({"phone": "12345678911111"}, "Phone number is too long"),
        ({"phone": "123"}, "Phone number is too short"),
        ({"name": "@#$"}, "name can contain only letters and '-' without whitespaces"),
        (
            {"surname": "@#$"},
            "surname can contain only letters and '-' without whitespaces",
        ),
        (
            {"ordering": "invalid ordering"},
            f"Ordering should be one of the following: ",
        ),
    ],
)
@pytest.mark.django_db
def test_owner_request_validation(
    api_client: APIClient, data: dict[str, str], expected_message: str
) -> None:
    ((key, value),) = data.items()
    if key == "ordering":
        owner_view = OwnerViewSet()
        ord_fields_string = ", ".join(owner_view.ordering_fields)
        expected_message += ord_fields_string

    response_get_owner_invalid_data = api_client.get(
        "/app/owners/", data=data, format="json"
    )
    assert response_get_owner_invalid_data.status_code == status.HTTP_400_BAD_REQUEST
    assert response_get_owner_invalid_data.data[key] == expected_message


@pytest.mark.parametrize(
    ("model_data", "model_str"),
    [
        ({"name": "Andrzej", "surname": "Starczyk", "phone": "575849675"}, "owner"),
        (
            {
                "brand": "Ford",
                "model": "Mondeo",
                "production_date": "2023-01-01",
            },
            "car",
        ),
    ],
)
@pytest.mark.django_db
def test_response_no_object_found(
    api_client: APIClient, model_data: dict[str, str], model_str: str
) -> None:
    response_get_model = api_client.get(
        f"/app/{model_str}s/", data=model_data, format="json"
    )
    assert response_get_model.status_code == status.HTTP_200_OK
    assert response_get_model.data == f"There is no {model_str.title()} with given data"


@pytest.mark.parametrize(
    ("data", "expected_message"),
    [
        (
            {"production_date": datetime.date.today() + datetime.timedelta(days=1)},
            "Production date cannot be from the future.",
        ),
        ({"ordering": "invalid ordering"}, "Ordering should be one of the following: "),
    ],
)
@pytest.mark.django_db
def test_car_request_validation(
    api_client: APIClient, data: dict[str, datetime.date | str], expected_message: str
) -> None:
    ((key, value),) = data.items()
    if key == "ordering":
        car_view = CarViewSet()
        ord_fields_string = ", ".join(car_view.ordering_fields)
        expected_message += ord_fields_string

    response_get_car_invalid_data = api_client.get(
        "/app/cars/", data=data, format="json"
    )
    assert response_get_car_invalid_data.status_code == status.HTTP_400_BAD_REQUEST
    assert response_get_car_invalid_data.data[key] == expected_message
