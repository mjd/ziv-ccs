# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):


    return render_to_response('index.html', {
        'title': 'Home Page',
        }, context_instance=RequestContext(request))
