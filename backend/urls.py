from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [

	        url(r'^admin-home$', views.admin_home,  name="admin_home"),
	        url(r'^admin/booking/category/(?P<status>.+)/$', views.admin_booking_category, name='admin_booking_category'),
	        url(r'^admin/search/$', views.search, name='search'),
			
	]