from typing import Final, final

from django.contrib.auth import models as auth_models
from django.db import models
from django_lifecycle import LifecycleModelMixin

from apps.helpers.managers import CustomFieldUserManager
from apps.helpers.models import UUIDModel

_FIELD_MAX_LENGTH: Final = 40


@final
class User(LifecycleModelMixin, UUIDModel, auth_models.AbstractUser):
    username = models.CharField('Имя пользователя', max_length=_FIELD_MAX_LENGTH, default='', blank=True)
    first_name = models.CharField('Имя', max_length=_FIELD_MAX_LENGTH, default='')
    email = models.EmailField('Адрес электронной почты', unique=True)
    is_active = models.BooleanField(default=True)
    objects = CustomFieldUserManager(username_field_name='email')  # noqa: WPS110

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]

    class Meta(auth_models.AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_username(self):
        # for jwt_payload_handler
        return str(self.first_name)

    def __str__(self):
        return self.first_name
