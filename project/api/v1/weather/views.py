from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.v1.weather.serializers import (
    CityDadataQuerySerializer,
    CityWeatherResultSerializer,
    CityReadSerializer, CityWeatherReadSerializer,
)
from apps.city.models import City
from apps.dadata.services import DadataCoordinatesByAddressService
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.weather.models import CityWeather


class CityWeatherViewSet(ExtendedModelViewSet):
    queryset = CityWeather.objects.all()
    serializer_class = CityWeatherReadSerializer
    serializer_class_map = {
        'read': CityWeatherReadSerializer,
    }
    search_fields = ('city__title', )
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        query_serializer=CityDadataQuerySerializer,
        responses={
            status.HTTP_200_OK: CityWeatherResultSerializer(many=True),
        },
    )
    @action(methods=['get'], detail=False, url_path='search_address')
    def search_address(self, request):  # noqa: WPS210
        """Вернет найденные варианты адресов."""
        query_serializer = CityDadataQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query = query_serializer.validated_data.get('query')
        result = DadataCoordinatesByAddressService().process(query_city=query)  # noqa: WPS110
        serializer = CityWeatherResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
