import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as authentication_jwt
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt import views

from apps.helpers import exceptions
from apps.helpers import serializers as serializers_helper
from apps.helpers.batchmixin import DeleteBatchMixin
from apps.helpers.custom_error import CustomValidationError
from apps.helpers.exceptions import ErrorResponseSerializer
from apps.helpers.viewsets import CRUExtendedModelViewSet
from apps.user.managers import UserManager
from apps.user.models import User

from . import serializers
from .filters import UserFilterSet
from .serializers import (
    UserReadSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()
logger = logging.getLogger()


class UserViewSet(views.TokenViewBase, CRUExtendedModelViewSet, DeleteBatchMixin):  # noqa: WPS338 WPS214
    queryset = User.objects.all()
    serializer_class = serializers.UserReadSerializer
    serializer_class_map = {
        'list': serializers.UserReadSerializer,
        'retrieve': serializers.UserReadSerializer,
        'me': serializers.UserReadSerializer,
        'login': jwt_serializers.TokenObtainPairSerializer,
        'refresh': jwt_serializers.TokenRefreshSerializer,
        'change_password': serializers.UserChangePasswordSerializer,
        'compact': serializers.UserCompactSerializer,
        'registration': serializers.UserRegistrationSerializer,
        'update': serializers.UserUpdateSerializer,
        'partial_update': serializers.UserUpdateSerializer,
    }
    permission_map = {
        'login': permissions.AllowAny,
        'send_code_registration': permissions.AllowAny,
        'registration': permissions.AllowAny,
    }
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication_jwt.JWTAuthentication, authentication.SessionAuthentication)
    filterset_class = UserFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    default_responses = {
        200: serializers.UserLoginResponseSerializer,
        400: ErrorResponseSerializer,
        410: ErrorResponseSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        return UserManager().get_queryset(user)

    def _auth(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.object.get('token')
        return Response({'token': token})

    @swagger_auto_schema(
        request_body=serializers.LoginSerializer,
        responses={status.HTTP_200_OK: jwt_serializers.TokenObtainPairSerializer},
    )
    @action(methods=['post'], detail=False)
    def login(self, request):
        if not User.objects.filter(email=request.data['email']).exists():
            raise CustomValidationError(
                {'detail': 'Не найдено', 'code': 'not_found'},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return super().post(request)  # noqa: WPS61311

    @swagger_auto_schema(responses={status.HTTP_200_OK: jwt_serializers.TokenObtainPairSerializer})
    @action(methods=['post'], detail=False)
    def refresh(self, request):
        return super().post(request)  # noqa: WPS613

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={201: UserReadSerializer, 400: exceptions.BadRequestResponseSerializer},
    )
    @action(methods=['post'], detail=False)
    def registration(self, request):
        """Register user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user, context=self.get_serializer_context()).data  # noqa: WPS110
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """Retrieve logged user information."""
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: serializers.UserChangePasswordSerializer, 400: ErrorResponseSerializer})
    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        """Change password."""
        serializer = self.get_serializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializers.UserReadSerializer(instance=user).data  # noqa: WPS110
        return Response(data)

    @action(methods=['get'], detail=False)
    def compact(self, request):
        """List compact user."""
        return super().list(request)  # noqa: WPS613


