from django.contrib import admin

from apps.city.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )
    search_fields = ('title',)

