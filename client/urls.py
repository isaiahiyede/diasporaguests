from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [

	        url(r'^client-page/$', views.client_page,  name="client_page"),
	        url(r'^booking/category/(?P<status>.+)/$', views.booking_category, name='booking_category'),
	        url(r'^client/search/$', views.search, name='search'),
	        url(r'^client/get-booking/$', views.get_booking, name='get_booking'),
	        url(r'^search-home/$', views.search_home, name='search_home'),

			
	]