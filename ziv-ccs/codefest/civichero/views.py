# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, CreateView

from models import Citizen
from forms import CitizenForm


def setup_view(request, title):

    return {
        'current_path': request.get_full_path(),
        'title': title,
    }

def home(request):
    context = setup_view(request, 'Home Page')

    return render_to_response('index.html', context, context_instance=RequestContext(request))


def friends(request):
    context = setup_view(request, 'Friends')

    return render_to_response('friends.html', context, context_instance=RequestContext(request))


def schedule(request):
    context = setup_view(request, 'Schedule')

    return render_to_response('schedule.html', context, context_instance=RequestContext(request))


def leaderboard(request):
    context = setup_view(request, 'Leaderboard')

    return render_to_response('leaderboard.html', context, context_instance=RequestContext(request))


def organizer_dashboard(request):
    context = setup_view(request, 'Organizer Dashboard')

    return render_to_response('organizer_dashboard.html', context, context_instance=RequestContext(request))


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
    context = setup_view(request, 'Checkin')

    return render_to_response('checkin.html', context, context_instance=RequestContext(request))



def login(request):
    context = setup_view(request, 'Login')

    return render_to_response('registration/login.html', context, context_instance=RequestContext(request))


#example of restricting access if we need to do that
#if not '@example.com' in request.user.email:
#    return HttpResponse("You can't vote in this poll.")

def register_user(request):

    context = setup_view(request, 'Register')

    if request.method == 'POST': # If the form has been submitted...
        form = CitizenForm(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass

            #Save the valid data
            citizen = form.save(commit=True)
            #registrant.registration_date = today
            #registrant.save()
            context['citizen'] = citizen

            return render_to_response('user_profile.html', context, context_instance=RequestContext(request))

    else:
        form = CitizenForm() # An unbound form

    context['form'] = form
    return render_to_response('create_user.html', context, context_instance=RequestContext(request))



class CitizenDetailView(DetailView):
    model = Citizen
    template_name = 'user_profile.html'

    # additional parameters
    username = None

    def get_object(self, queryset=None):

        self.username = self.kwargs['username']
        queryset = Citizen.objects.all()

        return queryset.get(user__username=self.username)


# class AuthorCreateView(CreateView):
#     form_class = CitizenForm
#     template_name = 'create_user.html'
#     success_url = 'success'