from rest_framework import serializers

from api.v1.city.serializers import CityReadSerializer
from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.weather.models import CityWeather


class CityWeatherReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    city = CityReadSerializer()
    select_related_fields = ("city",)

    class Meta:
        model = CityWeather
        fields = ('city', 'temperature', 'wind_speed',  'pressure')


class CityWeatherResultSerializer(serializers.Serializer):
    city = serializers.CharField()   # noqa: WPS110
    temperature = serializers.IntegerField()
    wind_speed = serializers.IntegerField()
    pressure = serializers.IntegerField()


class CityDadataQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
