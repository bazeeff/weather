from rest_framework import serializers

from apps.city.models import City


class CityReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'title', )


class CityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'title', )

