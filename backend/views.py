from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse , HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test
from general.models import *
from client.models import *
from general.forms import UserForm, UserAccountForm, LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from django.core import serializers
from django.db.models import Q
from django.contrib import messages
from django.template.context import RequestContext
from django.db.models import Count
from django import template
from itertools import chain
import re
import hashlib
import random, datetime
import urllib
import time
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
import json,random,string
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage, send_mail

# Create your views here.


@login_required
def admin_home(request):
	context = {}
	all_client_bookings = Bookings.objects.all()
	context['all_bookings_count'] = all_client_bookings.all().count()
	context['approved_bookings'] = all_client_bookings.filter(approved=True).count()
	context['processing_bookings'] = all_client_bookings.filter(approved=False).count()
	context['deleted_bookings'] = all_client_bookings.filter(deleted=True).count()
	context['completed_bookings'] = all_client_bookings.filter(approved=True, completed=True).count()
	context['total_payments'] = all_client_bookings.filter(approved=True).aggregate(Sum('amount_paid'))['amount_paid__sum']
	context['all_bookings'] = all_client_bookings
	template_name = 'backend/adminhome.html'
	return render(request,template_name,context)


@login_required
def admin_booking_category(request, status):
	context = {}
	all_client_bookings = Bookings.objects.all()
	context['all_bookings_count'] = all_client_bookings.all().count()
	context['approved_bookings'] = all_client_bookings.filter(approved=True).count()
	context['processing_bookings'] = all_client_bookings.filter(approved=False).count()
	context['deleted_bookings'] = all_client_bookings.filter(deleted=True).count()
	context['completed_bookings'] = all_client_bookings.filter(approved=True, completed=True).count()
	context['total_payments'] = all_client_bookings.filter(approved=True).aggregate(Sum('amount_paid'))['amount_paid__sum']

	approved = ''

	if status == 'processing':
		approved = False
		context['all_bookings'] = Bookings.objects.filter(approved=approved)
	elif status == 'approved':
		approved = True
		context['all_bookings'] = Bookings.objects.filter(approved=approved)
	elif status == 'completed':
		approved = True
		context['all_bookings'] = Bookings.objects.filter(approved=approved,completed=True)
	elif status == 'deleted':
		approved = True
		context['all_bookings'] = Bookings.objects.filter(deleted=True)
	else:
		context['all_bookings'] = Bookings.objects.all()
	
	template_name = template_name = 'backend/adminhome.html'
	return render(request,template_name,context)


@login_required
def search(request):

	context = {}

	all_client_bookings = Bookings.objects.all()
	context['all_bookings_count'] = all_client_bookings.all().count()
	context['approved_bookings'] = all_client_bookings.filter(approved=True).count()
	context['processing_bookings'] = all_client_bookings.filter(approved=False).count()
	context['deleted_bookings'] = all_client_bookings.filter(deleted=True).count()
	context['completed_bookings'] = all_client_bookings.filter(approved=True, completed=True).count()
	context['total_payments'] = all_client_bookings.filter(approved=True).aggregate(Sum('amount_paid'))['amount_paid__sum']
	
	if request.method == 'POST':
		rp = request.POST
		query = rp.get('srch-term')
		try:
			booking_obj = Bookings.objects.filter(Q(tracking_number__contains=query) | Q(ref_num__contains=query))
			context['all_bookings'] = booking_obj
		except:
			messages.info(request, "Search result does not match any avaliable booking")
			context['all_bookings'] = []


	template_name = template_name = 'backend/adminhome.html'
	return render(request,template_name,context)

















