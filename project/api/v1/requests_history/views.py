from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from api.v1.requests_history.serializers import RequestsHistoryReadSerializer
from apps.requests_history.models import RequestsHistory

from apps.helpers.viewsets import LRExtendedModelViewSet


class RequestsHistoryViewSet(LRExtendedModelViewSet):
    queryset = RequestsHistory.objects.all()
    serializer_class = RequestsHistoryReadSerializer
    serializer_class_map = {
        'read': RequestsHistoryReadSerializer,
        'retrieve': RequestsHistoryReadSerializer,
    }
    search_fields = ('city', )
    ordering_fields = ('city', 'created_at', )
    permission_classes = (IsAuthenticated,)
    filterset_fields = ['request_type', 'city']
