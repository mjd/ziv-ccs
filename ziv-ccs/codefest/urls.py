from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.views.generic import DetailView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ziv-ccs.views.home', name='home'),
    # url(r'^ziv-ccs/', include('ziv-ccs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

     (r'^/*$', 'civichero.views.home'),
     (r'^user/profile/(\w+)$', 'civichero.views.user_profile'),
     (r'^organizer/(\w+)/dashboard/*$', 'civichero.views.organizer_dashboard'),
     (r'^leaderboard/*$', 'civichero.views.leaderboard'),
     (r'^checkin/*$', 'civichero.views.checkin'),
     (r'^user/profile/(?P<screenname>[a-zA-Z0-9-]+)/$', CitizenDetailView.as_view(), name='user+profile'),

     #Auth
    #(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myapp/login.html'}),

    (r'^login$', 'django.contrib.auth.views.login'),
    (r'^users/login/$', 'civichero.views.login'),

)
