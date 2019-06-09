from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.conf import settings
import datetime
import markdown
from django.utils import timezone
from django.template.defaultfilters import slugify
# from modelchoices import TITLE, STATES, COUNTRY



# Create your models here.


class RoomType(models.Model):
	room_type    			= models.CharField(max_length=300, null=True, blank=True)
	room_description		= models.CharField(max_length=1500, null=True, blank=True)
	room_image            	= models.ImageField(upload_to="room_type", null=True, blank=True)
	room_price_1            = models.FloatField(max_length=50, default=0)
	room_service1			= models.CharField(max_length=500, null=True, blank=True)
	room_service2			= models.CharField(max_length=500, null=True, blank=True)
	room_service3			= models.CharField(max_length=500, null=True, blank=True)
	room_service4			= models.CharField(max_length=500, null=True, blank=True)
	room_service_others		= models.CharField(max_length=1500, null=True, blank=True)
	days_of_week            = models.CharField(max_length=200, null=True, blank=True)
	room_count              = models.PositiveIntegerField(default=1)


	class Meta:
	    verbose_name_plural = "RoomType"


	def __unicode__(self):
	    return '%s' %(self.room_type)


class RoomNumber(models.Model):
	room_number  =  models.CharField(max_length=30, null=True, blank=True)
	room_type    =  models.ForeignKey(RoomType, null=True,blank=True)
	booked       =  models.BooleanField(default=False) 


	class Meta:
	    verbose_name_plural = "RoomNumber"


	def __unicode__(self):
	    return '%s' %(self.room_number)
