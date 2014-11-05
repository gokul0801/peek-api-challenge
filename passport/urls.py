from django.conf.urls import patterns, url

urlpatterns = patterns('passport.views',
   url(r'^api/timeslots?date=(?P<date>.+)$', 'timeslots'), 
   url(r'^api/timeslots$', 'timeslots'),
   url(r'^api/boats$', 'boats'),
   url(r'^api/assignments$', 'assignments'),
   url(r'^api/bookings$', 'bookings'))
