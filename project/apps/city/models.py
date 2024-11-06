from typing import Final

from django.db import models

from apps.helpers.models import UUIDModel, CreatedModel

_FIELD_MAX_LENGTH: Final = 200


class City(UUIDModel):
    title = models.CharField('Название города из Дадаты', max_length=_FIELD_MAX_LENGTH)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.title
