import datetime
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from application.views import OwnerViewSet, CarViewSet


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def owner_data() -> dict[str, str]:
    owner_data = {"name": "Andrzej", "surname": "Starczyk", "phone": "575849675"}
    return owner_data


@pytest.fixture
def car_data(api_client: APIClient, owner_data: dict[str, str]) -> dict[str, str | int]:
    response_create_owner = api_client.post(
        "/app/owners/", data=owner_data, format="json"
    )
    owner_id = response_create_owner.data["id"]
    car_data = {
        "brand": "Ford",
        "model": "Mondeo",
        "production_date": "2023-01-01",
        "owner": owner_id,
    }

    return car_data


@pytest.mark.django_db
def test_create_and_get_owner(
    api_client: APIClient, owner_data: dict[str, str]
) -> None:
    # create owner
    response_create_owner = api_client.post(
        "/app/owners/", data=owner_data, format="json"
    )
    owner_id = response_create_owner.data["id"]
    assert response_create_owner.status_code == status.HTTP_201_CREATED
    assert all(
        [
            response_create_owner.data[key] == owner_data[key]
            for key in owner_data.keys()
        ]
    )

    # get owner
    response_get_owner = api_client.get(f"/app/owners/{owner_id}/", format="json")
    assert response_get_owner.status_code == status.HTTP_200_OK
    assert all(
        [response_get_owner.data[key] == owner_data[key] for key in owner_data.keys()]
    )


@pytest.mark.django_db
def test_patch_owner(api_client: APIClient, owner_data: dict[str, str]) -> None:
    # create owner
    response_create_owner = api_client.post(
        "/app/owners/", data=owner_data, format="json"
    )
    owner_id = response_create_owner.data["id"]
    assert response_create_owner.status_code == status.HTTP_201_CREATED
    assert all(
        [
            response_create_owner.data[key] == owner_data[key]
            for key in owner_data.keys()
        ]
    )

    # update owner
    owner_data["name"] = "Krzysztof"
    response_patch_owner = api_client.patch(
        f"/app/owners/{owner_id}/", data=owner_data, format="json"
    )
    assert response_patch_owner.status_code == status.HTTP_200_OK
    assert response_patch_owner.data["name"] == owner_data["name"]

    # owner does not exist
    response_patch_owner = api_client.patch(
        f"/app/owners/{owner_id + 1}/", data=owner_data, format="json"
    )
    assert response_patch_owner.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_owner(api_client: APIClient, owner_data: dict[str, str]) -> None:
    # create owner
    response_create_owner = api_client.post(
        "/app/owners/", data=owner_data, format="json"
    )
    owner_id = response_create_owner.data["id"]
    assert response_create_owner.status_code == status.HTTP_201_CREATED
    assert all(
        [
            response_create_owner.data[key] == owner_data[key]
            for key in owner_data.keys()
        ]
    )

    # delete owner
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


@pytest.mark.django_db
def test_create_and_get_car(
    api_client: APIClient, car_data: dict[str, str | int]
) -> None:
    # create car
    response_create_car = api_client.post("/app/cars/", data=car_data, format="json")
    car_id = response_create_car.data["id"]
    assert response_create_car.status_code == status.HTTP_201_CREATED
    assert all(
        [response_create_car.data[key] == car_data[key] for key in car_data.keys()]
    )

    # get car
    response_get_car = api_client.get(f"/app/cars/{car_id}/", format="json")
    assert response_get_car.status_code == status.HTTP_200_OK
    assert all([response_get_car.data[key] == car_data[key] for key in car_data.keys()])


@pytest.mark.django_db
def test_patch_car(api_client: APIClient, car_data: dict[str, str | int]) -> None:
    # create car
    response_create_car = api_client.post("/app/cars/", data=car_data, format="json")
    car_id = response_create_car.data["id"]
    assert response_create_car.status_code == status.HTTP_201_CREATED
    assert all(
        [response_create_car.data[key] == car_data[key] for key in car_data.keys()]
    )

    # update car
    car_data["production_date"] = "2023-06-10"
    response_patch_car = api_client.patch(
        f"/app/cars/{car_id}/", data=car_data, format="json"
    )
    assert response_patch_car.status_code == status.HTTP_200_OK
    assert response_patch_car.data["production_date"] == car_data["production_date"]

    # car does not exist
    response_patch_car = api_client.patch(
        f"/app/cars/{car_id + 1}/", data=car_data, format="json"
    )
    assert response_patch_car.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_car(api_client: APIClient, car_data: dict[str, str | int]) -> None:
    # create car
    response_create_car = api_client.post("/app/cars/", data=car_data, format="json")
    car_id = response_create_car.data["id"]
    assert response_create_car.status_code == status.HTTP_201_CREATED
    assert all(
        [response_create_car.data[key] == car_data[key] for key in car_data.keys()]
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
