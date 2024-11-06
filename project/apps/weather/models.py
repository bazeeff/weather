from typing import Final

from django.db import models

from apps.city.models import City

_FIELD_MAX_LENGTH: Final = 200

class CityWeather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.IntegerField("Температура в градусах цельсия", blank=True, null=True)
    pressure = models.IntegerField("Атмосферное давление", blank=True, null=True)
    wind_speed = models.IntegerField("Скорость ветра м/с", blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('last_updated',)
        verbose_name = 'Погода в городе'
        verbose_name_plural = 'Погода в городах'

    def __str__(self):
        return f'{self.city.title} температура {self.temperature} С, давление {self.pressure} мм рт.ст., скорость ветра {self.wind_speed} м/с'