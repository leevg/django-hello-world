from models import RequestInfo
from django.core.urlresolvers import reverse


class GetRequestsToDB(object):
    def process_request(self, request):
        method = request.META['REQUEST_METHOD']
        path = request.path
        if path != reverse('requests'):
            r = RequestInfo(method=method, path=path)
            r.save()
