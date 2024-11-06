# Generated by Django 5.1.2 on 2024-11-05 22:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestsHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('city', models.CharField(blank=True, max_length=150, null=True, verbose_name='Город из запроса')),
                ('request_type', models.CharField(choices=[('TG_API', 'Телеграм API-запрос'), ('WEB_API', 'Web-API-запрос')], default='WEB_API', max_length=7, verbose_name='Тип запроса')),
            ],
            options={
                'verbose_name': 'Запрос к API',
                'verbose_name_plural': 'Запросы к API',
            },
        ),
    ]
