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
def client_page(request):
	if request.user.is_staff:
		return redirect(reverse('backend:admin_home'))
	context = {}
	client_bookings= Bookings.objects.filter(user=request.user)
	context['all_bookings_count'] = client_bookings.all().count()
	context['approved_bookings'] = client_bookings.filter(approved=True).count()
	context['processing_bookings'] = client_bookings.filter(approved=False).count()
	context['deleted_bookings'] = client_bookings.filter(deleted=True).count()
	context['completed_bookings'] = client_bookings.filter(approved=True, completed=True).count()
	context['total_payments'] = client_bookings.filter(approved=True).aggregate(Sum('amount_paid'))['amount_paid__sum']
	context['all_bookings'] = Bookings.objects.filter(user=request.user)
	template_name = 'client/clientindex.html'
	return render(request,template_name,context)


@login_required
def booking_category(request, status):
	context = {}
	client_bookings = Bookings.objects.filter(user=request.user)
	context['all_bookings_count'] = client_bookings.all().count()
	context['approved_bookings'] = client_bookings.filter(approved=True).count()
	context['processing_bookings'] = client_bookings.filter(approved=False).count()
	context['deleted_bookings'] = client_bookings.filter(deleted=True).count()
	context['completed_bookings'] = client_bookings.filter(approved=True, completed=True).count()
	context['total_payments'] = client_bookings.filter(approved=True).aggregate(Sum('amount_paid'))['amount_paid__sum']

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
	
	template_name = template_name = 'client/clientindex.html'
	return render(request,template_name,context)


@login_required
def search(request):

	context = {}

	client_bookings = Bookings.objects.filter(user=request.user)
	context['all_bookings_count'] = client_bookings.all().count()
	context['approved_bookings'] = client_bookings.filter(approved=True).count()
	context['processing_bookings'] = client_bookings.filter(approved=False).count()
	context['deleted_bookings'] = client_bookings.filter(deleted=True).count()
	context['completed_bookings'] = client_bookings.filter(approved=True, completed=True).count()
	context['total_payments'] = client_bookings.filter(approved=True).aggregate(Sum('amount_paid'))['amount_paid__sum']
	
	rp = request.POST
	query = rp.get('srch-term')
	try:
		booking_obj = Bookings.objects.filter(Q(tracking_number__contains=query) | Q(ref_num__contains=query) ,Q(user=request.user))
		context['all_bookings'] = booking_obj
	except:
		messages = "Search query does not match any avaliable booking"
		context['messages'] = messages
		context['all_bookings'] = []

	template_name = template_name = 'client/clientindex.html'
	return render(request,template_name,context)


@login_required
def get_booking(request):
	context = {}
	template_name = 'client_snippets/bookingSummary.html'
	if request.method == 'GET':
		tracking_number = request.GET.get('tracking_number')
		booking_obj = Bookings.objects.get(tracking_number=tracking_number)
		context['reservation'] = booking_obj
		return render(request,template_name,context)
	return render(request,template_name,context)


def search_home(request):
	context = {}
	rp = request.POST
	print rp
	query = rp.get('srch-term-home')
	try:
		booking_obj = Bookings.objects.filter(Q(tracking_number__contains=query) | Q(ref_num__contains=query))
		context['reservation'] = booking_obj[0]
	except:
		message = "Search query does not match any avaliable booking"
		context['message'] = message

	template_name = 'general/search.html'
	return render(request,template_name,context)
















