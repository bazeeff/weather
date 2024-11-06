from django.utils.deprecation import MiddlewareMixin

from apps.requests_history.models import RequestsHistory, RequestTypeChoices


class RequestsHistoryMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if '/api/v1/weather/search_address/' in request.path and request.method == 'GET':
            city_name = request.GET.get('query')
            if city_name:
                request_type = RequestTypeChoices.WEB_API if 'HTTP_COOKIE' in request.META else RequestTypeChoices.TG_API
                RequestsHistory.objects.create(city=city_name, request_type=request_type)
