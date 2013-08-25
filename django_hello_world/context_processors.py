from django.conf import settings

def context_processor(request):
    return {'settings': settings}