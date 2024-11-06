from typing import Dict, List

import httpx
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.city.models import City
from apps.helpers.services import AbstractService
from apps.weather.models import CityWeather
from settings import API_SECRET_DADATA, API_TOKEN_DADATA, API_YANDEX_WEATHER_KEY
import requests


class DadataSearchAddressService(AbstractService):
    """Сервис по поиску адресов в Dadata."""

    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {API_TOKEN_DADATA}",
        "X-Secret": API_SECRET_DADATA
    }

    base_url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address'

    def transform_response(self, response: List[Dict]) -> List[Dict]:
        print(response)
        return [
            {
                'value': r['value'],
                'unrestricted_value': r['unrestricted_value'],
                'city_fias_id': r['data']['city_fias_id'],
                'settlement_fias_id': r['data']['settlement_fias_id'],
                'geo_lat': r['data']['geo_lat'],
                'geo_lon': r['data']['geo_lon'],

            }
            for r in response
        ]

    def process(self, query=None) -> List[Dict]:
        if query:
            client = httpx.Client(base_url=self.base_url, headers=self.headers)
            response = client.post(self.base_url, json={
                "query": f"{query}",
                "from_bound": {"value": "city"},
                "to_bound": {"value": "settlement"},
            })
            data = response.json()
            response = data.get("suggestions")

            # https://github.com/hflabs/dadata-py

            # from dadata import Dadata
            # token = API_TOKEN_DADATA
            # secret = API_SECRET_DADATA
            # dadata = Dadata(token, secret)
            # response = dadata.clean("address", query)
            if response is None:
                raise ValidationError("Город не найден")
            else:
                return self.transform_response(response)


class DadataCoordinatesByAddressService(AbstractService):

    def process(self, query_city=None):
        if not query_city:
            raise ValidationError("Название города не указано.")

        # Получаем координаты города с помощью Dadata
        lat, lon = self.get_coordinates(query_city)
        if lat is None or lon is None:
            raise ValidationError("Город не найден.")

        # Проверка, есть ли данные в кэше
        city_weather = self.get_cached_weather(query_city)
        if city_weather:
            return self.format_weather_data(city_weather)
        # Получаем данные о погоде из Yandex
        weather_data = self.get_weather_data(lat, lon)

        # Сохраняем данные о погоде в базе данных
        city_weather = self.save_weather_data(query_city, weather_data)
        return self.format_weather_data(city_weather)

    def format_weather_data(self, city_weather):
        """Форматирует данные о погоде для сериализации."""
        return {
            'city': city_weather.city.title,
            'temperature': city_weather.temperature,
            'pressure': city_weather.pressure,
            'wind_speed': city_weather.wind_speed,
        }

    def get_coordinates(self, query_city):
        """Получает координаты города с помощью Dadata API."""
        from dadata import Dadata
        dadata = Dadata(API_TOKEN_DADATA, API_SECRET_DADATA)
        response = dadata.clean("address", query_city)

        return response.get('geo_lat'), response.get('geo_lon')

    def get_weather_data(self, lat, lon):
        """Получает данные о погоде из Yandex Weather API по координатам."""
        headers = {'X-Yandex-Weather-Key': API_YANDEX_WEATHER_KEY}

        query = f"""
        {{
            weatherByPoint(request: {{ lat: {lat}, lon: {lon} }}) {{
                now {{
                    temperature
                    pressure
                    windSpeed
                    windDirection
                }}
            }}
        }}
        """

        response = requests.post(
            'https://api.weather.yandex.ru/graphql/query',
            headers=headers,
            json={'query': query}
        )
        response_data = response.json()

        return {
            'temperature': response_data['data']['weatherByPoint']['now']['temperature'],
            'pressure': response_data['data']['weatherByPoint']['now']['pressure'],
            'wind_speed': response_data['data']['weatherByPoint']['now']['windSpeed'],
            'wind_direction': response_data['data']['weatherByPoint']['now']['windDirection']
        }

    def get_cached_weather(self, query_city):
        """Проверяет кэшированные данные о погоде для города, если обновление было менее 30 минут назад."""
        try:
            city = City.objects.get(title=query_city)
            city_weather = CityWeather.objects.filter(city=city).latest('last_updated')
            if city_weather and (timezone.now() - city_weather.last_updated).total_seconds() < 1800:
                return city_weather  # Возвращаем кэшированные данные
        except City.DoesNotExist:
            pass
        return None

    def save_weather_data(self, query_city, weather_data):
        """Сохраняет данные о погоде в базе данных и возвращает запись."""
        city, _ = City.objects.get_or_create(title=query_city)
        city_weather = CityWeather.objects.create(
            city=city,
            temperature=weather_data['temperature'],
            pressure=weather_data['pressure'],
            wind_speed=weather_data['wind_speed']
        )
        return city_weather
