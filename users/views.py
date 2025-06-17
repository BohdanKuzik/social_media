from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema, OpenApiExample

from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    API endpoint for creating new users.

    Creates a new user account with the provided credentials.
    """

    serializer_class = UserSerializer

    @extend_schema(
        summary="Create a new user",
        description="Creates a new user account with email and password",
        request=UserSerializer,
        responses={201: UserSerializer},
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "email": "user@example.com",
                    "username": "username",
                    "password": "securepassword123",
                },
                status_codes=["201"],
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreateTokenView(ObtainAuthToken):
    """
    API endpoint for obtaining authentication tokens.

    Provides token-based authentication for users.
    """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    @extend_schema(
        summary="Obtain authentication token",
        description="Returns an authentication token for the provided credentials",
        request=ObtainAuthToken.serializer_class,
        responses={
            200: {"type": "object", "properties": {"token": {"type": "string"}}}
        },
        examples=[
            OpenApiExample(
                "Example Request",
                value={"username": "user@example.com", "password": "securepassword123"},
                status_codes=["200"],
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
