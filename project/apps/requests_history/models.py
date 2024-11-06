from django.db import models

from apps.helpers.models import UUIDModel, CreatedModel, enum_max_length


class RequestTypeChoices(models.TextChoices):
    TG_API = 'TG_API', 'Телеграм API-запрос'
    WEB_API = 'WEB_API', 'Web-API-запрос'


class RequestsHistory(UUIDModel, CreatedModel):
    city = models.CharField('Город из запроса', max_length=150, null=True, blank=True)
    request_type = models.CharField(
        "Тип запроса",
        max_length=enum_max_length(RequestTypeChoices),
        choices=RequestTypeChoices.choices,
        default=RequestTypeChoices.WEB_API,
    )

    def __str__(self):
        return f"{self.city} - {self.request_type} - {self.created_at}"

    class Meta:
        verbose_name = 'Запрос к API'
        verbose_name_plural = 'Запросы к API'
