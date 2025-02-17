import datetime
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from application.models import Owner, Car
from application.serializers import OwnerSerializer, CarSerializer
from application.views import OwnerViewSet, CarViewSet


class TestsOwnerViews:
    @pytest.mark.django_db
    def test_create_owner(
        self, api_client: APIClient, valid_owner_data: dict[str, str]
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
        self, api_client: APIClient, valid_owner_model_data: Owner
    ) -> None:
        owner_id = valid_owner_model_data.id
        # get owner
        response_get_owner = api_client.get(f"/app/owners/{owner_id}/", format="json")
        serializer = OwnerSerializer(valid_owner_model_data)
        assert response_get_owner.status_code == status.HTTP_200_OK
        assert response_get_owner.data == serializer.data

    @pytest.mark.django_db
    def test_patch_owner(
        self,
        api_client: APIClient,
        valid_owner_model_data: Owner,
        valid_new_owner_data: dict[str, str],
    ) -> None:
        # update owner
        owner_id = valid_owner_model_data.id
        response_patch_owner = api_client.patch(
            f"/app/owners/{owner_id}/", data=valid_new_owner_data, format="json"
        )
        assert response_patch_owner.status_code == status.HTTP_200_OK
        assert all(
            [
                response_patch_owner.data[key] == valid_new_owner_data[key]
                for key in valid_new_owner_data.keys()
            ]
        )

    @pytest.mark.django_db
    def test_delete_owner(
        self, api_client: APIClient, valid_owner_model_data: Owner
    ) -> None:
        # delete owner
        owner_id = valid_owner_model_data.id
        response_delete_owner = api_client.delete(
            f"/app/owners/{owner_id}/", format="json"
        )
        assert response_delete_owner.status_code == status.HTTP_204_NO_CONTENT

        # try to get that owner
        response_get_owner = api_client.get(f"/app/owners/{owner_id}/", format="json")
        assert response_get_owner.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        ("data", "expected_message"),
        [
            ({"phone": "asd1234cvb"}, "Phone number can contain only digits"),
            ({"phone": "12345678911111"}, "Phone number is too long"),
            ({"phone": "123"}, "Phone number is too short"),
            (
                {"name": "@#$"},
                "name can contain only letters and '-' without whitespaces",
            ),
            (
                {"surname": "@#$"},
                "surname can contain only letters and '-' without whitespaces",
            ),
            (
                {"ordering": "invalid ordering"},
                f"Ordering should be one of the following: {', '.join(OwnerViewSet().ordering_fields)}",
            ),
        ],
    )
    @pytest.mark.django_db
    def test_owner_request_validation(
        self, api_client: APIClient, data: dict[str, str], expected_message: str
    ) -> None:
        ((key, value),) = data.items()
        response_get_owner_invalid_data = api_client.get(
            "/app/owners/", data=data, format="json"
        )
        assert (
            response_get_owner_invalid_data.status_code == status.HTTP_400_BAD_REQUEST
        )
        assert response_get_owner_invalid_data.data[key] == expected_message

    @pytest.mark.django_db
    def test_owner_not_exist(
        self,
        api_client: APIClient,
        valid_owner_model_data: Owner,
        valid_new_owner_data: dict[str, str],
    ) -> None:
        # owner does not exist
        owner_id = valid_owner_model_data.id
        response_patch_owner = api_client.patch(
            f"/app/owners/{owner_id + 1}/", data=valid_new_owner_data, format="json"
        )
        response_delete_owner = api_client.delete(
            f"/app/owners/{owner_id + 1}/", format="json"
        )
        assert response_patch_owner.status_code == status.HTTP_404_NOT_FOUND
        assert response_delete_owner.status_code == status.HTTP_404_NOT_FOUND


class TestsCarViews:
    @pytest.mark.django_db
    def test_create_car(
        self, api_client: APIClient, valid_car_view_data: dict[str, str | int]
    ) -> None:
        # create car
        response_create_car = api_client.post(
            "/app/cars/", data=valid_car_view_data, format="json"
        )
        assert response_create_car.status_code == status.HTTP_201_CREATED
        assert all(
            [
                response_create_car.data[key] == valid_car_view_data[key]
                for key in valid_car_view_data.keys()
            ]
        )

    @pytest.mark.django_db
    def test_get_car(self, api_client: APIClient, valid_car_model_data: Car) -> None:
        # get car
        car_id = valid_car_model_data.id
        response_get_car = api_client.get(f"/app/cars/{car_id}/", format="json")
        serializer = CarSerializer(valid_car_model_data)
        assert response_get_car.data == serializer.data

    @pytest.mark.django_db
    def test_patch_car(
        self,
        api_client: APIClient,
        valid_car_model_data: Car,
        valid_new_car_view_data: dict[str, str | int],
    ) -> None:
        # update car
        car_id = valid_car_model_data.id
        response_patch_car = api_client.patch(
            f"/app/cars/{car_id}/", data=valid_new_car_view_data, format="json"
        )
        assert response_patch_car.status_code == status.HTTP_200_OK
        assert all(
            [
                response_patch_car.data[key] == valid_new_car_view_data[key]
                for key in valid_new_car_view_data.keys()
            ]
        )

    @pytest.mark.django_db
    def test_delete_car(self, api_client: APIClient, valid_car_model_data: Car) -> None:
        # delete car
        car_id = valid_car_model_data.id
        response_delete_car = api_client.delete(f"/app/cars/{car_id}/", format="json")
        assert response_delete_car.status_code == status.HTTP_204_NO_CONTENT

        # try to get that car
        response_get_car = api_client.get(f"/app/cars/{car_id}/", format="json")
        assert response_get_car.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        ("data", "expected_message"),
        [
            (
                {"production_date": datetime.date.today() + datetime.timedelta(days=1)},
                "Production date cannot be from the future.",
            ),
            (
                {"ordering": "invalid ordering"},
                f"Ordering should be one of the following: {', '.join(CarViewSet().ordering_fields)}",
            ),
        ],
    )
    @pytest.mark.django_db
    def test_car_request_validation(
        self,
        api_client: APIClient,
        data: dict[str, datetime.date | str],
        expected_message: str,
    ) -> None:
        ((key, value),) = data.items()
        response_get_car_invalid_data = api_client.get(
            "/app/cars/", data=data, format="json"
        )
        assert response_get_car_invalid_data.status_code == status.HTTP_400_BAD_REQUEST
        assert response_get_car_invalid_data.data[key] == expected_message

    @pytest.mark.django_db
    def test_car_not_exist(
        self,
        api_client: APIClient,
        valid_car_model_data: Car,
        valid_new_car_view_data: dict[str, str | int],
    ) -> None:
        # car does not exist
        car_id = valid_car_model_data.id
        response_patch_car = api_client.patch(
            f"/app/cars/{car_id + 1}/", data=valid_new_car_view_data, format="json"
        )
        response_delete_car = api_client.delete(
            f"/app/cars/{car_id + 1}/", format="json"
        )
        assert response_patch_car.status_code == status.HTTP_404_NOT_FOUND
        assert response_delete_car.status_code == status.HTTP_404_NOT_FOUND


class TestsCommon:
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
        self, api_client: APIClient, model_data: dict[str, str], model_str: str
    ) -> None:
        response_get_model = api_client.get(
            f"/app/{model_str}s/", data=model_data, format="json"
        )
        assert response_get_model.status_code == status.HTTP_200_OK
        assert (
            response_get_model.data
            == f"There is no {model_str.title()} with given data"
        )
