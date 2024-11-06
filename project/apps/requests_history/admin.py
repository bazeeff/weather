from django.contrib import admin

from apps.requests_history.models import RequestsHistory

@admin.register(RequestsHistory)
class RequestsHistoryAdmin(admin.ModelAdmin):
    pass
