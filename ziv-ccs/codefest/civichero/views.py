# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import DetailView
from datetime import datetime

from models import Citizen, Achievable, Activity, ActivityRecord, Event
from forms import CitizenForm, LocationForm


def setup_view(request, title):
    context = {
        'current_path': request.get_full_path(),
        'title': title,
        'citizen': None,
    }
    user = request.user

    if request.user.is_authenticated():
        citizens = Citizen.objects.filter(user=user)
        if 0 < len(citizens):
            citizen = Citizen.objects.get(user=user)
            context['citizen'] = citizen
            context['point_totals'] = citizen.getPointTotals()

    return context


def getActivityLocations():

    activities = Activity.objects.all()
    location_infos = []

    for activity in activities:
        location_infos.append( (str(activity.name), activity.location) )

    return location_infos


def home(request):
    context = setup_view(request, 'Home Page')
    citizen = context['citizen']

    if None == citizen:
        return redirect(login)

    friend_plans = citizen.getFriendsPlannedEvents()
    location_infos = getActivityLocations()

    context['home_location'] = citizen.home_location
    context['location_infos'] = location_infos
    context['friend_plans'] = friend_plans

    return render_to_response('index.html', context, context_instance=RequestContext(request))

@login_required(login_url='/user/login/')
def friends(request):
    context = setup_view(request, 'Friends')

    citizen = context['citizen']
    context['friends'] = citizen.friends.all()
    context['civic_zero'] = len(context['friends'])<= 0

    return render_to_response('friends.html', context, context_instance=RequestContext(request))

def about(request):
    context = setup_view(request, 'About')

    return render_to_response('about.html', context, context_instance=RequestContext(request))

def legal(request):
    context = setup_view(request, 'legal')

    return render_to_response('legal.html', context, context_instance=RequestContext(request))


def schedule(request):
    context = setup_view(request, 'Schedule')
    citizen = context['citizen']
    if None == citizen:
        return redirect(login)

    plans = citizen.getPlannedEvents()
    context['home_location'] = citizen.home_location
    context['plans'] = plans

    return render_to_response('schedule.html', context, context_instance=RequestContext(request))


def scheduleGraph(request):
    context = setup_view(request, 'ScheduleGraph')

    return render_to_response('scheduleGraph.html', context, context_instance=RequestContext(request))


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
def checkin(request, activity_id):

    context = setup_view(request, 'Checkin')
    activity_id = int(activity_id)
    user = request.user
    citizen = Citizen.objects.get(user=user)
    activity = Activity.objects.get(id=activity_id)
    civic_type = activity.civic_type

    now = datetime.now()

    #See if there is already a planned record for this
    records = ActivityRecord.objects.filter(citizen=citizen, activity=activity)

    if 0 <= len(records):
        record = ActivityRecord.objects.create(citizen=citizen, activity=activity, timestamp=now,
                                               civic_type=civic_type, status=ActivityRecord.COMPLETED)
    else:
        record = records[0]
        record.status = ActivityRecord.COMPLETED
        record.save()

    context['record'] = record

    #Now update acheivements
    context['new_achievments'] = citizen.checkAchievments(new_only=True)

    return render_to_response('checkin.html', context, context_instance=RequestContext(request))


@login_required(login_url='/user/login/')
def add_planned(request, event_id):

    context = setup_view(request, 'Add to Plan')
    event_id = int(event_id)
    user = request.user
    citizen = Citizen.objects.get(user=user)
    event = Event.objects.get(id=event_id)
    civic_type = event.civic_type

    now = datetime.now()

    records = ActivityRecord.objects.filter(citizen=citizen, activity=event)

    if 0 <= len(records):

        record = ActivityRecord.objects.create(citizen=citizen, activity=event, timestamp=now,
                                               civic_type=civic_type, status=ActivityRecord.PLANNED)

        context['record'] = record
    else:
        context['record'] = records[0]

    return render_to_response('addplanned.html', context, context_instance=RequestContext(request))



def login(request):
    context = setup_view(request, 'Login')

    return render_to_response('registration/login.html', context, context_instance=RequestContext(request))



#example of restricting access if we need to do that
#if not '@example.com' in request.user.email:
#    return HttpResponse("You can't vote in this poll.")

def register_user(request):

    context = setup_view(request, 'Register')

    if request.method == 'POST': # If the form has been submitted...
        citizen_form = CitizenForm(request.POST, request.FILES) # A form bound to the POST data
        location_form = LocationForm(request.POST)

        if citizen_form.is_valid() and location_form.is_valid(): # All validation rules pass

            #Save the valid data
            home_location = location_form.save(commit=True)
            user = citizen_form.save(commit=False)

            email = citizen_form.cleaned_data.get('email')
            avatar = citizen_form.cleaned_data.get('avatar')
            first_name = citizen_form.cleaned_data.get('first_name')
            last_name = citizen_form.cleaned_data.get('last_name')

            citizen = Citizen.objects.create(email=email, first_name=first_name, last_name=last_name, avatar=avatar,
                                             user=user, home_location=home_location)
            citizen.save()

            context['citizen'] = citizen

            return redirect(home)

    else:
        citizen_form = CitizenForm() # An unbound form
        location_form = LocationForm()

    context['citizen_form'] = citizen_form
    context['location_form'] = location_form
    return render_to_response('registration/create_user.html', context, context_instance=RequestContext(request))



class CitizenDetailView(DetailView):
    model = Citizen
    template_name = 'user_profile.html'

    # additional parameters
    username = None

    def get_object(self, queryset=None):

        self.username = self.kwargs['username']
        queryset = Citizen.objects.all()

        return queryset.get(user__username=self.username)


#AchievableDetailView
class AchievableDetailView(DetailView):
    model = Achievable
    template_name = 'achievable_details.html'

    # additional parameters
    name = None

    def get_object(self, queryset=None):

        self.name = self.kwargs['name']
        queryset = Achievable.objects.all()

        return queryset.get(name=self.name)


#AchievableDetailView
class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity.html'

    activity_id = None

    def get_object(self, queryset=None):

        self.activity_id = self.kwargs['activity_id']
        queryset = Activity.objects.all()

        return queryset.get(id=self.activity_id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        activity = Activity.objects.get(id=self.activity_id)

        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'event.html'

    event_id = None

    def get_object(self, queryset=None):

        self.event_id = self.kwargs['event_id']
        queryset = Event.objects.all()

        return queryset.get(id=self.event_id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EventDetailView, self).get_context_data(**kwargs)

        event = Event.objects.get(id=self.event_id)
        now = datetime.now()
        has_started = event.start_date <= now.date() and event.start_time <= now.time()


        # Add in a QuerySet of all the books
        context['has_started'] = has_started

        return context


# class AuthorCreateView(CreateView):
#     form_class = CitizenForm
#     template_name = 'create_user.html'
#     success_url = 'success'

