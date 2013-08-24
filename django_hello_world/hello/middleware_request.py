import datetime
from models import RequestInfo
class GetRequestsToDB(object):
    def process_request(self,request):
        method = request.META['REQUEST_METHOD']
        path = request.path
        if path != '/requests/':
            r = RequestInfo(method=method,path=path)
            r.save()

