import json
from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
import models


REFRESH_INTERVAL = 60000


def index(req):
    template = loader.get_template('messages/index.html')
    context = RequestContext(req, {'interval': REFRESH_INTERVAL})
    return HttpResponse(template.render(context))
    

def stats(req):
    response_data = {}
    try:
        response_data['result'] = 'success'
        response_data['cities'] = models.Messages.get_city_count()
        response_data['users'] = models.Messages.get_user_count()
        return HttpResponse(json.dumps(response_data), content_type="application/json") 
    except Exception as e:
        response_data['result'] = 'error'
        response_data['error'] = e.message
        return HttpResponse(json.dumps(response_data), content_type="application/json")
