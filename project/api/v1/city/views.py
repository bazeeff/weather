from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.city.serializers import (
    CityReadSerializer,
    CityWriteSerializer,
)
from apps.city.models import City
from apps.helpers.viewsets import ExtendedModelViewSet


class CityViewSet(ExtendedModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityReadSerializer
    serializer_class_map = {
        'read': CityReadSerializer,
        'create': CityWriteSerializer,
        'update': CityWriteSerializer,
    }
    search_fields = ('title', )
    ordering_fields = ('title', )
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=CityWriteSerializer,
        responses={
            status.HTTP_201_CREATED: CityReadSerializer(many=True),
        },
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CityReadSerializer(instance).data, status=status.HTTP_201_CREATED)


