from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.views.generic import DetailView
from civichero.views import CitizenDetailView
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ziv-ccs.views.home', name='home'),
    # url(r'^ziv-ccs/', include('ziv-ccs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^/*$', RedirectView.as_view(url='/home')),
    (r'^home/*$', 'codefest.civichero.views.home'),
    (r'^schedule/*$', 'codefest.civichero.views.schedule'),
    (r'^friends/*$', 'codefest.civichero.views.friends'),
    (r'^leaderboard/*$', 'codefest.civichero.views.leaderboard'),

    (r'^organizer/(\w+)/dashboard/*$', 'codefest.civichero.views.organizer_dashboard'),
    (r'^checkin/*$', 'codefest.civichero.views.checkin'),

    (r'^user/register/', CitizenDetailView.as_view()),
    (r'^user/profile/(?P<username>[a-zA-Z0-9-]+)/$', CitizenDetailView.as_view()),

    #Auth
    #(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myapp/login.html'}),

    (r'^login$', 'django.contrib.auth.views.login'),
    (r'^users/login/$', 'codefest.civichero.views.login'),

)
