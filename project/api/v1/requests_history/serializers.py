from rest_framework import serializers

from apps.requests_history.models import RequestsHistory, RequestTypeChoices
from apps.helpers.serializers import EnumSerializer, EnumField


class RequestsHistoryReadSerializer(serializers.ModelSerializer):
    request_type = EnumField(enum_class=RequestTypeChoices)

    class Meta:
        model = RequestsHistory
        fields = ('id', 'city', 'request_type', 'created_at',)
