from django.contrib import admin

from apps.weather.models import CityWeather


@admin.register(CityWeather)
class CityAdmin(admin.ModelAdmin):
    pass

