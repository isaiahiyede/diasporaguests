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
# from client.models import *
from backend.models import *


# Create your models here.


class UserAccount(models.Model):
    user                     = models.OneToOneField(User, null=True, blank=True)
    password2                = models.CharField(max_length=50, blank=True, null=True)
    phone_number             = models.CharField(max_length = 15, null = True, blank = True)
    created_on               = models.DateTimeField(null=True, blank=True)
    edited_on            	 = models.DateTimeField(null=True, blank=True)
    deleted_on               = models.DateTimeField(null=True, blank=True)
    updated_on               = models.DateTimeField(null=True, blank=True)      
    booking                  = models.ForeignKey('Bookings', null=True, blank=True)


    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Useraccount"

    def __unicode__(self):
        return '%s %s' %(self.user.first_name.upper(), self.user.last_name.upper())


class Bookings(models.Model):
    user                     = models.ForeignKey(User, null=True, blank=True)
    tracking_number          = models.CharField(max_length=30, null=True, blank=True)
    created_on               = models.DateTimeField(auto_now_add = True)
    checK_in                 = models.CharField(max_length=30, null=True, blank=True)
    checK_out                = models.CharField(max_length=30, null=True, blank=True)
    checked_out              = models.BooleanField(default = False)
    status                   = models.CharField(max_length=30, default="New")
    ref_num   				 = models.CharField(max_length=30, null=True, blank=True)
    days					 = models.CharField(max_length=30, null=True, blank=True)
    paid					 = models.BooleanField(default = False)
    approved                 = models.BooleanField(default = False)
    room_type                = models.CharField(max_length=30, null=True, blank=True)
    room_id                  = models.CharField(max_length=30, null=True, blank=True)
    amount_paid              = models.IntegerField(null=True, blank=True)
    completed                = models.BooleanField(default = False)
    deleted                  = models.BooleanField(default = False)
    # new_booking              = models.BooleanField(default=True)
    room_number              = models.CharField(max_length=30, null=True, blank=True)

    
    
    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Bookings"
    
    def __unicode__(self):
        return '%s' %(self.tracking_number)











