from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [

	        url(r'^$', views.homepage,  name="homepage"),
	        url(r'^signup/Page/$', views.userregister,  name="userregister"),
			url(r'^login/Page/$', views.userlogin,  name="login"),
            url(r'^logout/$', views.user_logout, name='user_logout'),
            url(r'^bookings/(?P<room_id>[-\w]+)/$', views.booking, name='make_booking'),
            url(r'^action/(?P<status>.+)/(?P<booking_id>[-\w]+)/$', views.action_taken, name='action_taken'),
            url(r'^create_booking/$', views.create_booking, name='create_booking'),
            url(r'^successful_registration/$', views.successful_registration, name='successful_registration'),
            
			
	]