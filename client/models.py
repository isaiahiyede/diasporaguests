from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.conf import settings
import datetime
import markdown
from django.utils import timezone
from django.template.defaultfilters import slugify
from general.models import *

# Create your models here.


class ClientBookings(models.Model):
	user                     = models.ForeignKey(User, null=True, blank=True)
	booking_number           = models.ForeignKey("general.Bookings", null=True, blank=True)

	class Meta:
	    verbose_name_plural = "Client Bookings"

	def __unicode__(self):
	    return '%s %s' %(self.user.first_name.upper(), self.user.last_name.upper())

