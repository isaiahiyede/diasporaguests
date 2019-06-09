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
# from matchingApp.models import MessageCenterComment
# from lvtvAdmin.views import paginate_list
# from lvtvguinea.settings import EMAIL_HOST_USER
# Create your views here.


def homepage(request):
	context = {}
	room_types = RoomType.objects.all()
	context['rooms'] = room_types
	template_name = 'general/homepage.html'
	return render(request, template_name, context)


def userlogin(request):
	context = {}
	username  = ""
	context['login_form'] = LoginForm()

	if request.method == "POST":
	    form = LoginForm(data = request.POST)

	    if form.is_valid:
	        email    = request.POST.get('email').strip()
	        password = request.POST.get('password').strip()
	        
	        user_account =  User.objects.filter((Q(email= email) | Q(useraccount__phone_number=email)))
	        
	        if not user_account.exists():
				context['email_not_found'] = True
				context['email'] = email
				return render(request, 'general/login.html', context )

	        if user_account.exists():
	            username = user_account[0].username
	        auth_user = authenticate(username = username, password = password)

	        if auth_user is not None:
	            user = auth_user

	            if user.is_active:
	                login(request, user)                    

	                if user.is_staff:
	                    response =  redirect(reverse('backend:admin_home'))
	                    return response
	                   
	                else:
	                    response = redirect(reverse("client:client_page"))
	                    return response
	        else:
	            # print "No details found for %s" %(email)
	            context['no_record_found'] = True
	        return render(request, 'general/login.html', context )
	else:
		return render(request, 'general/login.html',context)
	# context = {}
	# template_name = 'general/login.html'
	# return render(request, template_name, context)


def userregister(request):
	print "Got here"
	context = {}	
	
	user_form = UserForm()
	user_account_form = UserAccountForm()
	
	context['user_form'] = user_form
	context['user_account_form'] = user_account_form
	
	if  request.method            ==     "POST":
		rp                         =     request.POST
		print "rp:",rp	        
		userform                   =     UserForm(request.POST)
		user_account_form          =     UserAccountForm(request.POST)
		print "here1"
		if User.objects.filter(username = rp.get('username')).exists():                
			return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'username_is_taken':True})
		if User.objects.filter(email = rp.get('email')).exists():                
			return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'email_is_taken':True})
		if UserAccount.objects.filter(phone_number = rp.get('phone_number')).exists():
			return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'phone_is_taken':True})
		else:
			print "here2"
			if userform.is_valid and user_account_form.is_valid:
				print "here3"
				password1     = rp.get('password')
				password2     = rp.get('confirm_password')
				if password1 != password2:
					return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'password_mismatch':True})
				if len(password1) < 6:
					return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'password_too_short':True})
				user = User.objects.create(username = rp.get('username'), email = rp.get('email').lower(),
					first_name = rp.get('first_name'), last_name = rp.get('first_name'))
				user.set_password(rp.get('password')) 
				user.save()
				print 'here4'
				new_user_account = UserAccount.objects.create(
					user = user,
					phone_number = rp.get('phone_number'),
					created_on   = datetime.datetime.now())
				print 'here5'
				context['user_is_created']  =    True
				context['email']            =    rp.get('email')
				print "user creation for %s successful" %(user)
				return redirect(reverse('general:successful_registration'))
			else:
				print "errors detected"                    
				return render(request, 'general/register.html', context)  
	
		return redirect(request.META['HTTP_REFERER'])
	else:
		return render(request, 'general/register.html',context)


def user_logout(request):
	response = redirect(reverse('general:homepage'))
	logout(request)
	return response


def create_booking_number(value):
	allowed_chars = ''.join((string.uppercase, string.digits))
	unique_id = ''.join(random.choice(allowed_chars) for _ in range(9))
	return value + unique_id


def successful_registration(request):
    context = {}    
    return render(request, 'general/successful.html', context)



def booking(request,room_id):
	context = {}
	if request.user.is_staff:
		return redirect(reverse('backend:admin_home'))
	else:
		room_type = RoomType.objects.get(id=room_id)
		context['room_numbers'] = room_type.roomnumber_set.all()
		context['room_type'] = room_type
		return render(request,'general/bookRoom.html', context)



def create_booking(request):
	if request.method == "POST":
		context = {}
		rp = request.POST
		print rp

		from_date = (datetime.datetime.strptime(str(rp.get('from')), '%m/%d/%Y'))

		try:
			end_date = (datetime.datetime.strptime(str(rp.get('to')), '%m/%d/%Y'))
		except:
			end_date = rp.get('to')

		print from_date, end_date
		print type(from_date)

		current_time = datetime.datetime.now()
		print current_time

		if str(end_date) == "" and (str(from_date) > str(current_time)):
			days = 1

		elif str(end_date) == "" and (str(from_date) < str(current_time)):
			days = 0
			messages.warning(request,'Check in date is less than current time and date!!!')
			return redirect(request.META.get('HTTP_REFERER'))

		elif rp.get('from') == rp.get('to'):
			days = 0
			messages.warning(request,'check in date cannot be same as check out date!!!')
			return redirect(request.META.get('HTTP_REFERER'))

		elif rp.get('to') < rp.get('from'):
			days = 0
			messages.warning(request,'check in date cannot be greater than check out date!!!')
			return redirect(request.META.get('HTTP_REFERER'))

		elif (str(from_date) or str(end_date)) < str(current_time):
			days = 0
			messages.warning(request,'Oops it seems the check in date or check out dates is less than current time and date!!!')
			return redirect(request.META.get('HTTP_REFERER'))


		room_type = RoomType.objects.get(id=rp.get('room_type_id')).room_type
		room_number = RoomNumber.objects.get(id=rp.get('room_number')).room_number

		# from_dt = datetime.datetime.strptime(str(rp.get('from')), '%m-%d-%Y %H:%M:%S').strftime('%A')

		try:
			active_bookings = Bookings.objects.filter(room_id=rp.get('room_type_id'), new_booking=True)
		except Exception as e:
			pass 


		for booking in active_bookings:

			book_in_date = datetime.datetime.strptime(str(booking.checK_in), '%Y-%m-%d %H:%M:%S')
			
			book_out_date = datetime.datetime.strptime(str(booking.checK_out), '%Y-%m-%d %H:%M:%S')
			
			try:
				if booking.room_number == room_number:
					if (book_in_date <= from_date <= book_out_date):
						messages.warning(request,'Room already booked for check in date please select another room or date')
						return redirect(request.META.get('HTTP_REFERER'))
					else:
						pass
			except Exception as e:
				pass

		amount = float(rp.get('room_cost')) * float(rp.get('nod'))

		try:

			create_booking = Bookings.objects.create(
				user=request.user,
				tracking_number=create_booking_number('DPS-BKN'),
				ref_num=rp.get('pay_ref'),
				checK_in = from_date,
				checK_out = end_date,
				room_type = room_type,
				room_id = rp.get('room_type_id'),
				room_number = room_number,
				days=rp.get('nod'),
				amount_paid=amount)

			messages.success(request,'Well done! You successfully created a booking!!!')
			return redirect(reverse('client:client_page'))

		except:

			create_booking = Bookings.objects.create(
				tracking_number=create_booking_number('DPS-BKN'),
				ref_num=rp.get('pay_ref'),
				checK_in = from_date,
				checK_out = end_date,
				room_type = room_type,
				room_id = rp.get('room_type_id'),
				room_number = room_number,
				days=rp.get('nod'),
				amount_paid=amount)

			template_name = 'client/anonymous_booking.html'
			context['reservation'] = create_booking
			return render(request,template_name,context)

	return render(request.META['HTTP_REFERER'])


@login_required
def action_taken(request,status,booking_id):
	booking_obj = Bookings.objects.get(id=booking_id)
	if status == 'unapprove':
		booking_obj.approved = False
		booking_obj.status = 'Processing'
		booking.new_booking = True
		messages.info(request,'Booking Status has been changed successfully')
		booking_obj.save()
	elif status == 'approve':
		booking_obj.approved = True
		booking_obj.status = 'Approved'
		booking.new_booking = False
		messages.info(request,'Booking Status has been changed successfully')
		booking_obj.save()
	elif status == 'complete':
		booking_obj.completed = True
		booking_obj.status = 'Completed'
		booking.new_booking = False
		messages.info(request,'Booking Status has been changed successfully')
		booking_obj.save()
	else:
		booking_obj.deleted = True
		booking.new_booking = False
		messages.info(request,'Booking Status has been deleted successfully')
		booking_obj.save()
	return redirect(request.META.get('HTTP_REFERER'))



		































