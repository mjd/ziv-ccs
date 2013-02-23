# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView

from models import Citizen


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


# @login_required(login_url='/user/login/')
# def user_profile(request, screenName):
#
#     citizen = models.Citizen.objects.get(screen_name=screenName)
#
#     citizen_id = citizen.id
#
#     return CitizenDetailView.as_view(id=citizen_id)


@login_required(login_url='/user/login/')
def checkin(request):


    return render_to_response('checkin.html', {
        'title': 'Checkin',
        }, context_instance=RequestContext(request))



def login(request):

    return render_to_response('registration/login.html', {
        'title': 'Login',
        }, context_instance=RequestContext(request))


class CitizenDetailView(DetailView):
    model = Citizen
    #template_name = 'user_profile.html'

    # additional parameters
    screen_name = None

    def get_object(self, queryset=None):

        self.screen_name = self.kwargs['screenname']

        queryset = Citizen.objects.all()

        return queryset.get(screen_name=self.screen_name)
