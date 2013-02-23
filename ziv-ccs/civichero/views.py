# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):


    return render_to_response('index.html', {
        'title': 'Home Page',
        }, context_instance=RequestContext(request))

def organizer_dashboard(request):


    return render_to_response('organizer_dashboard.html', {
        'title': 'Organizer Dashboard',
        }, context_instance=RequestContext(request))

def leaderboard(request):


    return render_to_response('leaderboard.html', {
        'title': 'Leaderboard',
        }, context_instance=RequestContext(request))

def user_profile(request):


    return render_to_response('user_profile.html', {
        'title': 'Profile',
        }, context_instance=RequestContext(request))

def checkin(request):


    return render_to_response('checkin.html', {
        'title': 'Checkin',
        }, context_instance=RequestContext(request))
