from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


swagger_decorator_owner = swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            "id",
            in_=openapi.IN_PATH,
            description="Owner's unique id number",
            type=openapi.TYPE_INTEGER,
        )
    ])
swagger_decorator_car = swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            "id",
            in_=openapi.IN_PATH,
            description="Car's unique id number",
            type=openapi.TYPE_INTEGER,
        )
    ])
