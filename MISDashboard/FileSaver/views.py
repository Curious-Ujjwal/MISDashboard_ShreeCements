import os
import email
import numpy
import imaplib
import webbrowser
import pandas as pd
from .models import *
from datetime import date
from decimal import Decimal
from .defineconstants import *
from django.shortcuts import render
from email.header import decode_header
from django.template import RequestContext
from django.contrib.auth import login, authenticate

from .utilityfunction import *

# #account credentials
username = 'ujjwalrustagi@gmail.com'
password = 'Ujjwal@123'

# #function to create the folder name
def clean(text):
	return "".join(c if c.isalnum() else "_" for c in text)

# # Create your views here.
def download_files():
	#connect with IMAP class with SSL and authenticate
	imap = imaplib.IMAP4_SSL("imap.gmail.com")
	imap.login(username, password)

	status, messages = imap.select('INBOX')

	#select top 9 messages to download each day
	# 5 site reports and 4 wms reports
	N = 9

	today = date.today().strftime('%d-%m-%Y')
	print(today)

	#search for the SiteSheets folder in the MIS project
	path = os.getcwd()+"\..\SiteSheets"
	os.chdir(path)
	os.mkdir(today)			#move to the SiteSheets folder

	#total number of messages
	messages = int(messages[0])

	#iterating the MAILBOX from top to bottom for the top 'N' messages
	for i in range(messages, messages-N, -1):
		#fetch the email, message by ID
		#standard format => RFC822
		res, msg = imap.fetch(str(i), "(RFC822)")
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				subject, encoding = decode_header(msg["Subject"])[0]
				if isinstance(subject, bytes):
					subject = subject.decode(encoding)

				From, encoding = decode_header(msg.get("From"))[0]
				if isinstance(From, bytes):
					From = From.decode(encoding)

				#prints the subject and from ids at the terminal
				print("Subject:", subject)
				print("From:", From)

				#if the mail contains the many parts
				if msg.is_multipart():
					for part in msg.walk():
						content_type = part.get_content_type()
						content_disposition = str(part.get("Content-Disposition"))
						body = None
						try:
							body = part.get_payload(decode=True).decode()
						except:
							pass

						if content_type == "text/plain" and "attachment" not in content_disposition:
							print(body)

						elif "attachment" in content_disposition:
							filename = part.get_filename()

							# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ #
							# the specification for storing files and folders is missing
							# kindly complete this after the task of calculating the values if finished
							# folder_name pattern and file name pattern should be specified
							# folder names should consist of the site first name
							# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ #

							if filename:
								folder_name = clean(subject)
								if not os.path.isdir(folder_name):
									os.mkdir(folder_name)

								# filepath should be date/folder_name/filename
								filepath = os.path.join(folder_name, filename)

								open(filepath, "wb").write(part.get_payload(decode=True))
				else:
					content_type = msg.get_content_type()
					body = msg.get_payload(decode=True).decode()

					if content_type == "text/plain":
						print(body)
				print("^"*100)

	#reposition the directories at the end
	path = os.getcwd() + "\..\MISDashboard\FileSaver"
	os.chdir(path)

	#close the connection and logout
	imap.close()
	imap.logout()	


# #Site sheet and WMS sheet variables
# """
# 	siteP -> Panipat SiteSheet
# 	siteB -> Beawar SiteSheet
# 	siteJ -> Jharkhand SiteSheet
# 	siteC -> Castamet SiteSheet
# 	siteR -> Roorkee SiteSheet

# 	wmsC -> WMS Report of Castamet
# 	wmsJ -> WMS Report of Jharkhand
# 	wmsP -> WMS Report of Panipat
# 	wmsR -> WMS Report of Roorkee
# """

# #return the no. of days in a year based on if it is a leap/non-leap year
# # true -> leap year
# # false -> non-leap year
def calculate_days(date_year):
	if (date_year%4) == 0:
		if (date_year%100) == 0:
			if(date_year%400) == 0:
				return True
			else:
				return False
		else:
			return True
	else:
		return False

# #Day and month from date
today = date.today().strftime('%d-%m-%Y')
today1 = date.today()
date_day = int(today[:2])
date_month = int(today[3:5])
date_year = int(today[6:])
days_in_the_year = 366 if calculate_days(date_year) else 365
months_till_date = 0

#calculate months till date starting from April
months_till_date = (date_month + 12 - 3 + 1)%12

if months_till_date==0:
	months_till_date = 12


# #Data used for calculating seasonal tilt
#Admin can modify panipat_global_inclide for any excpected changes
panipat1_seasonal_tilt = None
panipat2_seasonal_tilt = None
roorkee_seasonal_tilt = None
jharkhand_seasonal_tilt = None
castamet_5deg_fix_tilt = None
beawar_seasonal_tilt = b_beawar_seasonal_tilt

if(calculate_days(date_year)):
	panipat1_seasonal_tilt = lp_panipat1_seasonal_tilt
	panipat2_seasonal_tilt = lp_panipat2_seasonal_tilt
	roorkee_seasonal_tilt = lp_roorkee_seasonal_tilt
	jharkhand_seasonal_tilt = lp_jharkhand_seasonal_tilt
	castamet_5deg_fix_tilt = lp_castamet_5deg_fix_tilt

else:
	panipat1_seasonal_tilt = nlp_panipat1_seasonal_tilt
	panipat2_seasonal_tilt = nlp_panipat2_seasonal_tilt
	roorkee_seasonal_tilt = nlp_roorkee_seasonal_tilt
	jharkhand_seasonal_tilt = nlp_jharkhand_seasonal_tilt
	castamet_5deg_fix_tilt = nlp_castamet_5deg_fix_tilt

#For panipat site using siteP datasheet and Panipat WMS report
def calculate_panipat_values():
	#Daily parameters calculation
	today_sum = 0.0
	monthly_sum = 0.0
	count_till_date = 0
	monthly_irradiance = 0.0
	user_input = 0.0
	deemed_loss_till_date = 0.0
	grid_loss_till_date = 0.0
	bd_loss_till_date = 0.0
	dust_loss_till_date = 0.0
	yearly_gen_till_date = 0.0
	month_irradiance_till_date = 0.0
	actual_irradiation_target_plf = 0.0
	p_rows, p_cols = siteP.shape

	for i in range(p_rows):
		today_sum += siteP[i][4]

	last_record = None
	count_till_date = 0
	monthly_sum = 0.0

	try:
		last_record = Panipat_Sheet.objects.latest('date')
		count_till_date = Panipat_Sheet.objects.all().count()
		print('Here')
		#check if the month is same
		last_record_month = int(last_record.date[3:5])
		if(date_month == last_record_month):
			monthly_sum = last_record.monthly_actual_generation + today_sum
			month_irradiance_till_date = last_record.monthly_actual_irradiance
			actual_irradiation_target_plf = last_record.irradiation_target_plf
		else:
			monthly_sum = today_sum

		yearly_gen_till_date = last_record.yearly_actual_generation + today_sum

		#this variable need to be calculated in admin.py file
		monthly_irradiance = (last_record.monthly_actual_irradiance)*count_till_date + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = last_record.monthly_deemed_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = last_record.monthly_grid_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = last_record.monthly_bd_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = last_record.monthly_dust_loss + user_input

	except:
		last_record = None
		print('Hereqkdgfckwq')
		count_till_date = 0
		monthly_sum = today_sum
		yearly_gen_till_date = today_sum

		#this needs to be calculated in admin.py file
		monthly_irradiance = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = user_input

	days_elapsed = count_till_date + 1 				#all the data is stored in sql db for a year
	print(days_elapsed)
	today_target_generation_value = 0.00
	today_actual_generation_value = today_sum
	today_target_plf = ((float(today_target_generation_value))/(panipat_constant*24))*100
	today_actual_plf = ((float(today_actual_generation_value))/(panipat_constant*24))*100
	today_target_irradiance = (panipat1_seasonal_tilt[date_month]*999.4 + panipat2_seasonal_tilt[date_month]*248)/panipat_constant
	today_actual_irradiance = 0.0 #from WMS report	
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*panipat_constant))*100
	today_actual_performance_ratio = 0.00
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user, in admin.py)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = 0.0	#given by the user
	today_deemed_loss_plf = ((float(today_deemed_loss_kwh))/(panipat_constant*24))*100	#in admin.py file
	today_grid_outage_loss_kwh = 0.0	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(panipat_constant*24))*100	#in admin.py file
	today_bd_loss_kwh = 0.0	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(panipat_constant*24))*100	#in admin.py file
	today_dust_loss_kwh = 0.0 #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(panipat_constant*24))*100	#in admin.py file
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly parameter values
	monthly_target_generation_value = today_target_generation_value*date_day
	monthly_actual_generation_value = monthly_sum
	monthly_target_plf = ((float(monthly_target_generation_value))/(panipat_constant*24*date_day))*100
	monthly_actual_plf = ((float(monthly_actual_generation_value))/(panipat_constant*24*date_day))*100
	monthly_target_irradiance = today_target_irradiance
	monthly_actual_irradiance = month_irradiance_till_date
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*panipat_constant))*100
	monthly_actual_performance_ratio = 0.00
	monthly_irradiance_loss = 0.0
	monthly_deemed_loss_kwh = 0.0	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh, in admin.py file
	monthly_deemed_loss_plf = ((float(monthly_deemed_loss_kwh))/(panipat_constant*24*date_day))*100	#in admin.py file
	monthly_grid_outage_loss_kwh = 0.0	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh, in admin.py file
	monthly_grid_outage_loss_plf = 0.0
	monthly_bd_loss_kwh = 0.0	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh, in admin.py file
	monthly_bd_loss_plf = ((float(monthly_bd_loss_kwh))/(panipat_constant*24*date_day))*100	#in admin.py file
	monthly_dust_loss_kwh = 0.0	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh, in 
	monthly_dust_loss_plf = ((float(monthly_dust_loss_kwh))/(panipat_constant*24*date_day))*100	#in admin.py file
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = 0.0
	yearly_actual_generation_value = yearly_gen_till_date
	yearly_target_plf = 0.00
	yearly_actual_plf = ((float(yearly_actual_generation_value))/(panipat_constant*24*days_elapsed))*100
	sumall = 100	#in admin.py file
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = sumall/(float(days_elapsed))		#in admin.py file

	avg1 = 0	#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt1
	avg2 = 0	#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt2

	i=0
	while i < months_till_date:
		avg1 = avg1 + panipat1_seasonal_tilt[(i+2)%12]
		avg2 = avg2 + panipat2_seasonal_tilt[(i+2)%12]
		i+=1
		

	avg1 = avg1/months_till_date
	avg2 = avg2/months_till_date

	yearly_target_irradiance = (avg1*999.4 + avg2*248)/panipat_constant
	yearly_target_performance_ratio = (float(yearly_target_generation_value)/(panipat_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = (float(yearly_actual_generation_value)/(panipat_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	gen = None
	#yearly_target_generation_value, gen is also calculated in admin.py file
	yearly_irradiance_loss = 0.00
	yearly_deemed_loss_kwh = sumall = 0.0
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day, calculated in admin.py file
	"""
	yearly_deemed_loss_plf = (float(yearly_deemed_loss_kwh)/(panipat_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall = 0.0
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day, calculated in admin.py file
	"""
	yearly_grid_outage_loss_plf = (float(yearly_grid_outage_loss_kwh)/(panipat_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall = 0.0
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day, calculated in admin.py file
	"""
	yearly_bd_loss_plf = (float(yearly_bd_loss_kwh)/(panipat_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall = 0.0
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day, calculated in admin.py file
	"""
	yearly_dust_loss_plf = (float(yearly_dust_loss_kwh)/(panipat_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf

	p = Panipat_Sheet(date=today1, 
					  days_elapsed= days_elapsed,
					  daily_target_generation=today_target_generation_value,
					  daily_actual_generation=today_actual_generation_value,
					  irradiation_target_plf=0.0,
					  kwh_target_plf=0.0,
					  monthly_target_generation=monthly_target_generation_value,
					  monthly_actual_generation=monthly_actual_generation_value,
					  yearly_target_generation=yearly_target_generation_value,
					  yearly_actual_generation=yearly_actual_generation_value,
					  daily_target_plf=today_target_plf,
					  daily_actual_plf=today_actual_plf,
					  monthly_target_plf=monthly_target_plf,
					  monthly_actual_plf=monthly_actual_plf,
					  yearly_target_plf=yearly_target_plf,
					  yearly_actual_plf=yearly_actual_plf,
					  daily_target_performance_ratio=today_target_performace_ratio,
					  daily_actual_performance_ratio=today_actual_performance_ratio,
					  monthly_target_performance_ratio=monthly_target_performance_ratio,
					  monthly_actual_performance_ratio=monthly_actual_performance_ratio,
					  yearly_target_performance_ratio=yearly_target_performance_ratio,
					  yearly_actual_performance_ratio=yearly_actual_performance_ratio,
					  daily_target_irradiance=today_target_irradiance,
					  daily_actual_irradiance=today_actual_irradiance,
					  monthly_target_irradiance=monthly_target_irradiance,
					  monthly_actual_irradiance=monthly_actual_irradiance,
					  yearly_target_irradiance=yearly_target_irradiance,
					  yearly_actual_irradiance=yearly_actual_irradiance,
					  daily_irradiance_loss=today_irradiance_loss,
					  monthly_irradiance_loss=actual_irradiation_target_plf,
					  yearly_irradiance_loss=yearly_irradiance_loss,
					  daily_deemed_loss=0.00,
					  monthly_deemed_loss=0.00,
					  yearly_deemed_loss=0.00,
					  daily_deemed_loss_plf=today_deemed_loss_plf,
					  monthly_deemed_loss_plf=monthly_deemed_loss_plf,
					  yearly_deemed_loss_plf=yearly_deemed_loss_plf,
					  daily_grid_loss=0.00,
					  monthly_grid_loss=0.00,
					  yearly_grid_loss=0.00,
					  daily_grid_loss_plf=today_grid_outage_loss_plf,
					  monthly_grid_loss_plf=monthly_grid_outage_loss_plf,
					  yearly_grid_loss_plf=yearly_grid_outage_loss_plf,
					  daily_bd_loss=0.00,
					  monthly_bd_loss=0.00,
					  yearly_bd_loss=0.00,
					  daily_bd_loss_plf=today_bd_loss_plf,
					  monthly_bd_loss_plf=monthly_bd_loss_plf,
					  yearly_bd_loss_plf=yearly_bd_loss_plf,
					  daily_dust_loss=0.00,
					  monthly_dust_loss=0.00,
					  yearly_dust_loss=0.00,
					  daily_dust_loss_plf=today_dust_loss_plf,
					  monthly_dust_loss_plf=monthly_dust_loss_plf,
					  yearly_dust_loss_plf=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	p.save()


#For castamet site using siteP datasheet and Castamet WMS report
def calculate_castamet_values():
	#Daily parameter values

	today_sum = 0.0
	monthly_sum = 0.0
	count_till_date = 0
	monthly_irradiance = 0.0
	user_input = 0.0
	deemed_loss_till_date = 0.0
	grid_loss_till_date = 0.0
	bd_loss_till_date = 0.0
	dust_loss_till_date = 0.0
	yearly_gen_till_date = 0.0
	month_irradiance_till_date = 0.0
	actual_irradiation_target_plf = 0.0
	c_rows, c_cols = siteC.shape

	for i in range(c_rows):
		today_sum += siteC[i][4]

	last_record = None
	count_till_date = 0
	monthly_sum = 0.0

	try:
		last_record = Castamet_Sheet.objects.latest('date')
		count_till_date = Castamet_Sheet.objects.all().count()
		#check if the month is same
		last_record_month = int(last_record.date[3:5])
		if(date_month == last_record_month):
			monthly_sum = last_record.monthly_actual_generation + today_sum
			month_irradiance_till_date = last_record.monthly_actual_irradiance
			actual_irradiation_target_plf = last_record.irradiation_target_plf
		else:
			monthly_sum = today_sum
		yearly_gen_till_date = last_record.yearly_actual_generation + today_sum

		#this variable need to be calculated in admin.py file
		monthly_irradiance = (last_record.monthly_actual_irradiance)*count_till_date + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = last_record.monthly_deemed_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = last_record.monthly_grid_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = last_record.monthly_bd_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = last_record.monthly_dust_loss + user_input

	except:
		last_record = None
		count_till_date = 0
		monthly_sum = today_sum
		yearly_gen_till_date = today_sum

		#this needs to be calculated in admin.py file
		monthly_irradiance = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = user_input

	days_elapsed = count_till_date + 1 				#all the data is stored in sql db for a year

	today_target_generation_value = 0.00
	today_actual_generation_value = today_sum
	today_target_plf = ((float(today_target_generation_value))/(castamet_constant*24))*100
	today_actual_plf = ((float(today_actual_generation_value))/(castamet_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = 0.0 #from WMS report	
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*castamet_constant))*100
	today_actual_performance_ratio = 0.0
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user, in admin.py)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = 0.0 	#user input
	today_deemed_loss_plf = ((float(today_deemed_loss_kwh))/(castamet_constant*24))*100 #, in admin.py
	today_grid_outage_loss_kwh = 0.0	#given by the user
	today_grid_outage_loss_plf = ((float(today_grid_outage_loss_kwh))/(castamet_constant*24))*100 #, in admin.py
	today_bd_loss_kwh = 0.0	#given by the user
	today_bd_loss_plf = ((float(today_bd_loss_kwh))/(castamet_constant*24))*100 #, in admin.py
	today_dust_loss_kwh = 0.0 #given by the user
	today_dust_loss_plf = ((float(today_dust_loss_kwh))/(castamet_constant*24))*100 #, in admin.py
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day
	monthly_actual_generation_value = monthly_sum
	monthly_target_plf = ((float(monthly_target_generation_value))/(castamet_constant*24*date_day))*100
	monthly_actual_plf = ((float(monthly_actual_generation_value))/(castamet_constant*24*date_day))*100
	monthly_target_irradiance = today_target_irradiance
	monthly_actual_irradiance = month_irradiance_till_date
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*castamet_constant))*100 #in admin.py file
	monthly_actual_performance_ratio = 0.0
	monthly_irradiance_loss = 0.0
	monthly_deemed_loss_kwh = 0.00	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh
	monthly_deemed_loss_plf = ((float(monthly_deemed_loss_kwh))/(castamet_constant*24*date_day))*100 #in admin.py file
	monthly_grid_outage_loss_kwh = 0.0	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh
	monthly_grid_outage_loss_plf = 0.0
	monthly_bd_loss_kwh = 0.0	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh
	monthly_bd_loss_plf = ((float(monthly_bd_loss_kwh))/(castamet_constant*24*date_day))*100 #in admin.py file
	monthly_dust_loss_kwh = 0.0	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh
	monthly_dust_loss_plf = ((float(monthly_dust_loss_kwh))/(castamet_constant*24*date_day))*100 #in admin.py file
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf #in admin.py file

	#Yearly parameter values
	yearly_target_generation_value = 0.0		#sum of all monthly_target_generation_value, in admin.py file
	yearly_actual_generation_value = yearly_gen_till_date
	yearly_target_plf = 0.0
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = ((float(yearly_actual_generation_value))/(castamet_constant*24*days_elapsed))*100
	sumall = 100	
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = sumall/(float(days_elapsed))
	
	avg1 = 0	#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt1
	
	i=0
	while(i < months_till_date):
		avg1 = avg1 + castamet_seasonal_tilt[(i+3)%12]
		i+=1
	avg1 = avg1/months_till_date

	yearly_target_irradiance = avg1
	yearly_target_performance_ratio = ((float(yearly_target_generation_value))/(castamet_constant*yearly_target_irradiance*days_elapsed))*100	#in admin.py file
	yearly_actual_performance_ratio = ((float(yearly_actual_generation_value))/(castamet_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	yearly_irradiance_loss = ((float(yearly_target_generation_value))/(castamet_constant*24*days_elapsed))*100 - ((float(gen))/(castamet_constant*24*days_elapsed))*100
	yearly_deemed_loss_kwh = sumall = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float(yearly_deemed_loss_kwh))/(castamet_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float(yearly_grid_outage_loss_kwh))/(castamet_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float(yearly_bd_loss_kwh))/(castamet_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float(yearly_dust_loss_kwh))/(castamet_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf	#in admin.py file

	c = Castamet_Sheet(date=today1, 
					  days_elapsed= days_elapsed,
					  daily_target_generation=today_target_generation_value,
					  daily_actual_generation=today_actual_generation_value,
					  irradiation_target_plf=0.0,
					  kwh_target_plf=0.0,
					  monthly_target_generation=monthly_target_generation_value,
					  monthly_actual_generation=monthly_actual_generation_value,
					  yearly_target_generation=yearly_target_generation_value,
					  yearly_actual_generation=yearly_actual_generation_value,
					  daily_target_plf=today_target_plf,
					  daily_actual_plf=today_actual_plf,
					  monthly_target_plf=monthly_target_plf,
					  monthly_actual_plf=monthly_actual_plf,
					  yearly_target_plf=yearly_target_plf,
					  yearly_actual_plf=yearly_actual_plf,
					  daily_target_performance_ratio=today_target_performace_ratio,
					  daily_actual_performance_ratio=today_actual_performance_ratio,
					  monthly_target_performance_ratio=monthly_target_performance_ratio,
					  monthly_actual_performance_ratio=monthly_actual_performance_ratio,
					  yearly_target_performance_ratio=yearly_target_performance_ratio,
					  yearly_actual_performance_ratio=yearly_actual_performance_ratio,
					  daily_target_irradiance=today_target_irradiance,
					  daily_actual_irradiance=today_actual_irradiance,
					  monthly_target_irradiance=monthly_target_irradiance,
					  monthly_actual_irradiance=monthly_actual_irradiance,
					  yearly_target_irradiance=yearly_target_irradiance,
					  yearly_actual_irradiance=yearly_actual_irradiance,
					  daily_irradiance_loss=today_irradiance_loss,
					  monthly_irradiance_loss=monthly_irradiance_loss,
					  yearly_irradiance_loss=yearly_irradiance_loss,
					  daily_deemed_loss=0.00,
					  monthly_deemed_loss=0.00,
					  yearly_deemed_loss=0.00,
					  daily_deemed_loss_plf=today_deemed_loss_plf,
					  monthly_deemed_loss_plf=monthly_deemed_loss_plf,
					  yearly_deemed_loss_plf=yearly_deemed_loss_plf,
					  daily_grid_loss=0.00,
					  monthly_grid_loss=0.00,
					  yearly_grid_loss=0.00,
					  daily_grid_loss_plf=today_grid_outage_loss_plf,
					  monthly_grid_loss_plf=monthly_grid_outage_loss_plf,
					  yearly_grid_loss_plf=yearly_grid_outage_loss_plf,
					  daily_bd_loss=0.00,
					  monthly_bd_loss=0.00,
					  yearly_bd_loss=0.00,
					  daily_bd_loss_plf=today_bd_loss_plf,
					  monthly_bd_loss_plf=monthly_bd_loss_plf,
					  yearly_bd_loss_plf=yearly_bd_loss_plf,
					  daily_dust_loss=0.00,
					  monthly_dust_los=0.00,
					  yearly_dust_loss=0.00,
					  daily_dust_loss_plf=today_dust_loss_plf,
					  monthly_dust_loss_plf=monthly_dust_loss_plf,
					  yearly_dust_loss_plf=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	c.save()


#For beawar site using siteB datasheet and Beawar WMS report
def calculate_beawar_values():
	#Daily parameter values
	today_sum = 0.0
	monthly_sum = 0.0
	count_till_date = 0
	monthly_irradiance = 0.0
	user_input = 0.0
	deemed_loss_till_date = 0.0
	grid_loss_till_date = 0.0
	bd_loss_till_date = 0.0
	dust_loss_till_date = 0.0
	yearly_gen_till_date = 0.0
	month_irradiance_till_date = 0.0
	actual_irradiation_target_plf = 0.0
	b_rows, b_cols = siteB.shape

	for i in range(b_rows):
		today_sum += siteB[i][3]

	last_record = None
	count_till_date = 0
	monthly_sum = 0.0

	try:
		last_record = Beawar_Sheet.objects.latest('date')
		count_till_date = Beawar_Sheet.objects.all().count()
		#check if the month is same
		last_record_month = int(last_record.date[3:5])
		if(date_month == last_record_month):
			monthly_sum = last_record.monthly_actual_generation + today_sum
			month_irradiance_till_date = last_record.monthly_actual_irradiance
			actual_irradiation_target_plf = last_record.irradiation_target_plf
		else:
			monthly_sum = today_sum
		yearly_gen_till_date = last_record.yearly_actual_generation + today_sum

		#this variable need to be calculated in admin.py file
		monthly_irradiance = (last_record.monthly_actual_irradiance)*count_till_date + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = last_record.monthly_deemed_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = last_record.monthly_grid_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = last_record.monthly_bd_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = last_record.monthly_dust_loss + user_input

	except:
		last_record = None
		count_till_date = 0
		monthly_sum = today_sum
		yearly_gen_till_date = today_sum

		#this needs to be calculated in admin.py file
		monthly_irradiance = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = user_input

	days_elapsed = count_till_date + 1 				#all the data is stored in sql db for a year

	today_target_generation_value = 0.00	#user input
	today_actual_generation_value = site5[4][3]
	today_target_plf = (float(today_target_generation_value)/(beawar_constant*24))*100
	today_actual_plf = (float(today_actual_generation_value)/(beawar_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = 0.0	#from WMS report
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*beawar_constant))*100	#in admin.py file
	today_actual_performance_ratio = ((float(today_actual_generation_value))/(today_actual_irradiance*beawar_constant))*100	#in admin.py file
	kwh_target_plf=site5[3][5]
	today_irradiance_loss = today_target_plf - kwh_target_plf #(value of Target PLF based on Actual Irradiation from the Beawar Sheet)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = 0.0	#given by the user	#in admin.py file
	today_deemed_loss_plf = (float(today_deemed_loss_kwh)/(castamet_constant*24))*100	#in admin.py file
	today_grid_outage_loss_kwh = 0.0	#given by the user	#in admin.py file
	today_grid_outage_loss_plf = (float(today_grid_outage_loss_kwh)/(castamet_constant*24))*100	#in admin.py file
	today_bd_loss_kwh = 0.0	#given by the user	#in admin.py file
	today_bd_loss_plf = (float(today_bd_loss_kwh)/(castamet_constant*24))*100	#in admin.py file
	today_dust_loss_kwh = 0.0 #given by the user	#in admin.py file
	today_dust_loss_plf = (float(today_dust_loss_kwh)/(castamet_constant*24))*100	#in admin.py file
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day #DOUBT
	monthly_actual_generation_value = monthly_sum
	monthly_target_plf = (float(monthly_target_generation_value)/(beawar_constant*24*date_day))*100
	monthly_actual_plf = (float(monthly_actual_generation_value)/(beawar_constant*24*date_day))*100
	monthly_target_irradiance = today_target_irradiance
	monthly_actual_irradiance = 0.0	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance, in admin.py file
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*beawar_constant))*100
	monthly_actual_performance_ratio = 0.0
	monthly_irradiance_loss = 0.0
	monthly_deemed_loss_kwh = 0.00
	monthly_deemed_loss_plf = ((float(monthly_deemed_loss_kwh))/(beawar_constant*24*date_day))*100	#in admin.py file
	monthly_grid_outage_loss_kwh = 0.0	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh	#in admin.py file
	monthly_grid_outage_loss_plf = 0.00
	monthly_bd_loss_kwh = float(0)	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh + sum of today_external_loss & prev. calculated monthly_external_loss	#in admin.py file
	monthly_bd_loss_plf = ((float(monthly_bd_loss_kwh))/(beawar_constant*24*date_day))*100	#in admin.py file
	monthly_dust_loss_kwh = 0.0	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh	#in admin.py file
	monthly_dust_loss_plf = ((float(monthly_dust_loss_kwh))/(beawar_constant*24*date_day))*100	#in admin.py file
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = 0.0		#sum of all monthly_target_generation_value OR sum of prev. stored yearly_target_generation_value + today_generation_value	#in admin.py file
	yearly_actual_generation_value = yearly_gen_till_date
	yearly_target_plf = 0.00
	yearly_actual_plf = ((float(yearly_actual_generation_value))/(beawar_constant*24*days_elapsed))*100
	sumall = 100		#in admin.py file
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = (sumall/(float(days_elapsed))) + 0.1	#in admin.py file

	avg1 = 0	#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt1
	
	i=0
	while(i < months_till_date):
		avg1 = avg1 + beawar_seasonal_tilt[(i+3)%12]
		i+=1
	avg1 = avg1/months_till_date


	yearly_target_irradiance = avg1 + 0.15
	yearly_target_performance_ratio = ((float(yearly_target_generation_value))/(beawar_constant*yearly_target_irradiance*days_elapsed))*100	#in admin.py file
	yearly_actual_performance_ratio = ((float(yearly_actual_generation_value))/(beawar_constant*yearly_actual_irradiance*days_elapsed))*100	#in admin.py file
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	gen = None	#in admin.py file
	yearly_irradiance_loss = 0.00
	yearly_deemed_loss_kwh = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float(yearly_deemed_loss_kwh))/(beawar_constant*24*days_elapsed))*100	#in admin.py file
	yearly_grid_outage_loss_kwh = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float(yearly_grid_outage_loss_kwh))/(beawar_constant*24*days_elapsed))*100	#in admin.py file
	yearly_bd_loss_kwh = 0.00	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh  + monthly_exteernal_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float(yearly_bd_loss_kwh))/(beawar_constant*24*days_elapsed))*100	#in admin.py file
	yearly_dust_loss_kwh = 0.00	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float(yearly_dust_loss_kwh))/(beawar_constant*24*days_elapsed))*100	#in admin.py file
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf	#in admin.py file

	b = Beawar_Sheet(date=today1, 
					  days_elapsed= days_elapsed,
					  daily_target_generation=today_target_generation_value,
					  daily_actual_generation=today_actual_generation_value,
					  irradiation_target_plf=0.0,
					  kwh_target_plf=site5[3][5],
					  monthly_target_generation=monthly_target_generation_value,
					  monthly_actual_generation=monthly_actual_generation_value,
					  yearly_target_generation=yearly_target_generation_value,
					  yearly_actual_generation=yearly_actual_generation_value,
					  daily_target_plf=today_target_plf,
					  daily_actual_plf=today_actual_plf,
					  monthly_target_plf=monthly_target_plf,
					  monthly_actual_plf=monthly_actual_plf,
					  yearly_target_plf=yearly_target_plf,
					  yearly_actual_plf=yearly_actual_plf,
					  daily_target_performance_ratio=today_target_performace_ratio,
					  daily_actual_performance_ratio=today_actual_performance_ratio,
					  monthly_target_performance_ratio=monthly_target_performance_ratio,
					  monthly_actual_performance_ratio=monthly_actual_performance_ratio,
					  yearly_target_performance_ratio=yearly_target_performance_ratio,
					  yearly_actual_performance_ratio=yearly_actual_performance_ratio,
					  daily_target_irradiance=today_target_irradiance,
					  daily_actual_irradiance=today_actual_irradiance,
					  monthly_target_irradiance=monthly_target_irradiance,
					  monthly_actual_irradiance=monthly_actual_irradiance,
					  yearly_target_irradiance=yearly_target_irradiance,
					  yearly_actual_irradiance=yearly_actual_irradiance,
					  daily_irradiance_loss=today_irradiance_loss,
					  monthly_irradiance_loss=monthly_irradiance_loss,
					  yearly_irradiance_loss=yearly_irradiance_loss,
					   daily_deemed_loss=0.00,
					  monthly_deemed_loss=0.00,
					  yearly_deemed_loss=0.00,
					  daily_deemed_loss_plf=today_deemed_loss_plf,
					  monthly_deemed_loss_plf=monthly_deemed_loss_plf,
					  yearly_deemed_loss_plf=yearly_deemed_loss_plf,
					  daily_grid_loss=0.00,
					  monthly_grid_loss=0.00,
					  yearly_grid_loss=0.00,
					  daily_grid_loss_plf=today_grid_outage_loss_plf,
					  monthly_grid_loss_plf=monthly_grid_outage_loss_plf,
					  yearly_grid_loss_plf=yearly_grid_outage_loss_plf,
					  daily_bd_loss=0.00,
					  monthly_bd_loss=0.00,
					  yearly_bd_loss=0.00,
					  daily_bd_loss_plf=today_bd_loss_plf,
					  monthly_bd_loss_plf=monthly_bd_loss_plf,
					  yearly_bd_loss_plf=yearly_bd_loss_plf,
					  daily_dust_loss=0.00,
					  monthly_dust_los=0.00,
					  yearly_dust_loss=0.00,
					  daily_dust_loss_plf=today_dust_loss_plf,
					  monthly_dust_loss_plf=monthly_dust_loss_plf,
					  yearly_dust_loss_plf=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	b.save()


#For roorkee site using siteR datasheet and Roorkee WMS report
def calculate_roorkee_values():
	#Daily parameter values
	
	today_sum = 0.0
	monthly_sum = 0.0
	count_till_date = 0
	monthly_irradiance = 0.0
	user_input = 0.0
	deemed_loss_till_date = 0.0
	grid_loss_till_date = 0.0
	bd_loss_till_date = 0.0
	dust_loss_till_date = 0.0
	yearly_gen_till_date = 0.0
	month_irradiance_till_date = 0.0
	actual_irradiation_target_plf = 0.0
	r_rows, r_cols = siteR.shape

	for i in range(r_rows):
		today_sum += siteR[i][4]

	last_record = None
	count_till_date = 0
	monthly_sum = 0.0

	try:
		last_record = Roorkee_Sheet.objects.latest('date')
		count_till_date = Roorkee_Sheet.objects.all().count()
		#check if the month is same
		last_record_month = int(last_record.date[3:5] )
		if(date_month == last_record_month):
			monthly_sum = last_record.monthly_actual_generation + today_sum
			month_irradiance_till_date = last_record.monthly_actual_irradiance
			actual_irradiation_target_plf = last_record.irradiation_target_plf
		else:
			monthly_sum = today_sum
		yearly_gen_till_date = last_record.yearly_actual_generation + today_sum

		#this variable need to be calculated in admin.py file
		monthly_irradiance = (last_record.monthly_actual_irradiance)*count_till_date + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = last_record.monthly_deemed_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = last_record.monthly_grid_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = last_record.monthly_bd_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = last_record.monthly_dust_loss + user_input

	except:
		last_record = None
		count_till_date = 0
		monthly_sum = today_sum
		yearly_gen_till_date = today_sum

		#this needs to be calculated in admin.py file
		monthly_irradiance = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = user_input

	days_elapsed = count_till_date + 1 				#all the data is stored in sql db for a year

	today_target_generation_value = 0.00
	today_actual_generation_value = today_sum
	today_target_plf = ((float(today_target_generation_value))/(roorkee_constant*24))*100
	today_actual_plf = ((float(today_actual_generation_value))/(roorkee_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = 0.0	#to be taken as an input from user OR from WMS report, in admin.py
	today_target_performace_ratio = 0.00
	today_actual_performance_ratio = 0.0
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = 0.0	#given by the user	#in admin.py file
	today_deemed_loss_plf = 0.00
	today_grid_outage_loss_kwh = 0.0	#given by the user	#in admin.py file
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(roorkee_constant*24))*100	#in admin.py file
	today_bd_loss_kwh = 0.0	#given by the user	#in admin.py file
	today_bd_loss_plf = (today_bd_loss_kwh/(roorkee_constant*24))*100	#in admin.py file
	today_dust_loss_kwh = 0.0 #given by the user	#in admin.py file
	today_dust_loss_plf = (today_dust_loss_kwh/(roorkee_constant*24))*100	#in admin.py file
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf	#in admin.py file

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day
	monthly_actual_generation_value = monthly_sum
	monthly_target_plf = ((float(monthly_target_generation_value))/(roorkee_constant*24*date_day))*100
	monthly_actual_plf = ((float(monthly_actual_generation_value))/(roorkee_constant*24*date_day))*100
	monthly_target_irradiance = today_target_irradiance
	monthly_actual_irradiance = 100.00	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance
	monthly_target_performance_ratio = 0.00
	monthly_actual_performance_ratio = 0.0
	monthly_irradiance_loss = 0.00
	monthly_deemed_loss_kwh = 0.00	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh	#in admin.py file
	monthly_deemed_loss_plf = ((float(monthly_deemed_loss_kwh))/(roorkee_constant*24*date_day))*100	#in admin.py file
	monthly_grid_outage_loss_kwh = 0.0	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh	#in admin.py file
	monthly_grid_outage_loss_plf = 0.00
	monthly_bd_loss_kwh = 0.0	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh	#in admin.py file
	monthly_bd_loss_plf = ((float(monthly_bd_loss_kwh))/(roorkee_constant*24*date_day))*100	#in admin.py file
	monthly_dust_loss_kwh = 0.0	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh	#in admin.py file
	monthly_dust_loss_plf = ((float(monthly_dust_loss_kwh))/(roorkee_constant*24*date_day))*100	#in admin.py file
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf		#in admin.py file
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf	#in admin.py file

	#Yearly parameter values
	yearly_target_generation_value = 0.0		#sum of all monthly_target_generation_value
	yearly_actual_generation_value = yearly_gen_till_date
	yearly_target_plf = 0.0
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = ((float(yearly_actual_generation_value))/(roorkee_constant*24*days_elapsed))*100
	sumall = 100	#in admin.py file
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = sumall/(float(days_elapsed))
	
	avg1 = 0	#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt1
	
	i=0
	while(i < months_till_date):
		avg1 = avg1 + roorkee_seasonal_tilt[(i+3)%12]
		i+=1

	avg1 = avg1/months_till_date

	yearly_target_irradiance = avg1
	yearly_target_performance_ratio = ((float(yearly_target_generation_value))/(roorkee_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = ((float(yearly_actual_generation_value))/(roorkee_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	yearly_irradiance_loss = 0.00
	yearly_deemed_loss_kwh = sumall	= 0.0 #in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float(yearly_deemed_loss_kwh))/(roorkee_constant*24*days_elapsed))*100	#in admin.py file
	yearly_grid_outage_loss_kwh = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float(yearly_grid_outage_loss_kwh))/(roorkee_constant*24*days_elapsed))*100	#in admin.py file
	yearly_bd_loss_kwh = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float(yearly_bd_loss_kwh))/(roorkee_constant*24*days_elapsed))*100	#in admin.py file
	yearly_dust_loss_kwh = 0.0	#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float(yearly_dust_loss_kwh))/(roorkee_constant*24*days_elapsed))*100	#in admin.py file
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf	#in admin.py file

	r = Roorkee_Sheet(date=today1,  
					  days_elapsed= days_elapsed,
					  daily_target_generation=today_target_generation_value,
					  daily_actual_generation=today_actual_generation_value,
					  irradiation_target_plf=0.0,
					  kwh_target_plf=0.0,
					  monthly_target_generation=monthly_target_generation_value,
					  monthly_actual_generation=monthly_actual_generation_value,
					  yearly_target_generation=yearly_target_generation_value,
					  yearly_actual_generation=yearly_actual_generation_value,
					  daily_target_plf=today_target_plf,
					  daily_actual_plf=today_actual_plf,
					  monthly_target_plf=monthly_target_plf,
					  monthly_actual_plf=monthly_actual_plf,
					  yearly_target_plf=yearly_target_plf,
					  yearly_actual_plf=yearly_actual_plf,
					  daily_target_performance_ratio=today_target_performace_ratio,
					  daily_actual_performance_ratio=today_actual_performance_ratio,
					  monthly_target_performance_ratio=monthly_target_performance_ratio,
					  monthly_actual_performance_ratio=monthly_actual_performance_ratio,
					  yearly_target_performance_ratio=yearly_target_performance_ratio,
					  yearly_actual_performance_ratio=yearly_actual_performance_ratio,
					  daily_target_irradiance=today_target_irradiance,
					  daily_actual_irradiance=today_actual_irradiance,
					  monthly_target_irradiance=monthly_target_irradiance,
					  monthly_actual_irradiance=monthly_actual_irradiance,
					  yearly_target_irradiance=yearly_target_irradiance,
					  yearly_actual_irradiance=yearly_actual_irradiance,
					  daily_irradiance_loss=today_irradiance_loss,
					  monthly_irradiance_loss=monthly_irradiance_loss,
					  yearly_irradiance_loss=yearly_irradiance_loss,
					  daily_deemed_loss=0.00,
					  monthly_deemed_loss=0.00,
					  yearly_deemed_loss=0.00,
					  daily_deemed_loss_plf=today_deemed_loss_plf,
					  monthly_deemed_loss_plf=monthly_deemed_loss_plf,
					  yearly_deemed_loss_plf=yearly_deemed_loss_plf,
					  daily_grid_loss=0.00,
					  monthly_grid_loss=0.00,
					  yearly_grid_loss=0.00,
					  daily_grid_loss_plf=today_grid_outage_loss_plf,
					  monthly_grid_loss_plf=monthly_grid_outage_loss_plf,
					  yearly_grid_loss_plf=yearly_grid_outage_loss_plf,
					  daily_bd_loss=0.00,
					  monthly_bd_loss=0.00,
					  yearly_bd_loss=0.00,
					  daily_bd_loss_plf=today_bd_loss_plf,
					  monthly_bd_loss_plf=monthly_bd_loss_plf,
					  yearly_bd_loss_plf=yearly_bd_loss_plf,
					  daily_dust_loss=0.00,
					  monthly_dust_loss=0.00,
					  yearly_dust_loss=0.00,
					  daily_dust_loss_plf=today_dust_loss_plf,
					  monthly_dust_loss_plf=monthly_dust_loss_plf,
					  yearly_dust_loss_plf=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	r.save()


#For jharkhand site using siteJ datasheet and Jharkhand WMS report
def calculate_jharkhand_values():
	#Daily parameter values
	today_sum = 0.0
	monthly_sum = 0.0
	count_till_date = 0
	monthly_irradiance = 0.0
	user_input = 0.0
	deemed_loss_till_date = 0.0
	grid_loss_till_date = 0.0
	bd_loss_till_date = 0.0
	dust_loss_till_date = 0.0
	yearly_gen_till_date = 0.0
	month_irradiance_till_date = 0.0
	actual_irradiation_target_plf = 0.0
	j_rows, j_cols = siteJ.shape

	for i in range(j_rows):
		today_sum += siteJ[i][4]

	last_record = None
	count_till_date = 0
	monthly_sum = 0.0

	try:
		last_record = Jharkhand_Sheet.objects.latest('date')
		count_till_date = Jharkhand_Sheet.objects.all().count()
		#check if the month is same
		last_record_month = int(last_record.date[3:5])
		if(date_month == last_record_month):
			monthly_sum = last_record.monthly_actual_generation + today_sum
			month_irradiance_till_date = last_record.monthly_actual_irradiance
			actual_irradiation_target_plf = last_record.irradiation_target_plf
		else:
			monthly_sum = today_sum
		yearly_gen_till_date = last_record.yearly_actual_generation + today_sum

		#this variable need to be calculated in admin.py file
		monthly_irradiance = (last_record.monthly_actual_irradiance)*count_till_date + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = last_record.monthly_deemed_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = last_record.monthly_grid_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = last_record.monthly_bd_loss + user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = last_record.monthly_dust_loss + user_input

	except:
		last_record = None
		count_till_date = 0
		monthly_sum = today_sum
		yearly_gen_till_date = today_sum

		#this needs to be calculated in admin.py file
		monthly_irradiance = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_deemed_loss_plf
		deemed_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_grid_loss_plf
		grid_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_bd_loss_plf
		bd_loss_till_date = user_input

		#this variable needs to be calculated in admin.py file, then calculate monthly_dust_loss_plf
		dust_loss_till_date = user_input

	days_elapsed = count_till_date + 1 				#all the data is stored in sql db for a year

	today_target_generation_value = 0.00	#this value is entered by user?
	today_actual_generation_value = today_sum
	today_target_plf = ((float(today_target_generation_value))/(jharkhand_constant*24))*100
	today_actual_plf = ((float(today_actual_generation_value))/(jharkhand_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = 0.0 #from WMS report	
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*jharkhand_constant))*100
	today_actual_performance_ratio = 0.00
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = 0.0	#given by the user
	today_deemed_loss_plf = ((float(today_deemed_loss_kwh))/(jharkhand_constant*24))*100
	today_grid_outage_loss_kwh = 0.0	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(jharkhand_constant*24))*100
	today_bd_loss_kwh = 0.0	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(jharkhand_constant*24))*100
	today_dust_loss_kwh = 0.0 #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(jharkhand_constant*24))*100
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day 
	monthly_actual_generation_value = monthly_sum
	monthly_target_plf = ((float(monthly_target_generation_value))/(jharkhand_constant*24*date_day))*100
	monthly_actual_plf = ((float(monthly_actual_generation_value))/(jharkhand_constant*24*date_day))*100
	monthly_target_irradiance = today_target_irradiance
	monthly_actual_irradiance = 0.00	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance #in admin.py file
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*jharkhand_constant))*100
	monthly_actual_performance_ratio = 0.00
	monthly_irradiance_loss = 0.0
	monthly_deemed_loss_kwh = 0.0	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh #in admin.py file
	monthly_deemed_loss_plf = ((float(monthly_deemed_loss_kwh))/(jharkhand_constant*24*date_day))*100 #in admin.py file
	monthly_grid_outage_loss_kwh = 0.0	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh #in admin.py file
	monthly_grid_outage_loss_plf = 0.0
	monthly_bd_loss_kwh = 0.0	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh #in admin.py file
	monthly_bd_loss_plf = ((float(monthly_bd_loss_kwh))/(jharkhand_constant*24*date_day))*100 #in admin.py file
	monthly_dust_loss_kwh = 0.0	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh #in admin.py file
	monthly_dust_loss_plf = ((float(monthly_dust_loss_kwh))/(jharkhand_constant*24*date_day))*100 #in admin.py file
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf #in admin.py file
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = 0.0		#sum of all monthly_target_generation_value
	yearly_actual_generation_value = yearly_gen_till_date
	yearly_target_plf = ((float(yearly_target_generation_value))/(jharkhand_constant*24*days_elapsed))*100
	yearly_actual_plf = ((float(yearly_actual_generation_value))/(jharkhand_constant*24*days_elapsed))*100
	sumall = 100	 #in admin.py file
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = sumall/(float(days_elapsed))
	
	avg1 = 0	#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt1
	
	i=0
	while(i < months_till_date):
		avg1 = avg1 + jharkhand_seasonal_tilt[(i+3)%12]
		i+=1

	avg1 = avg1/months_till_date

	yearly_target_irradiance = avg1
	yearly_target_performance_ratio = ((float(yearly_target_generation_value))/(jharkhand_constant*yearly_target_irradiance*days_elapsed))*100 #in admin.py file
	yearly_actual_performance_ratio = ((float(yearly_actual_generation_value))/(jharkhand_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	yearly_irradiance_loss = 0.00
	yearly_deemed_loss_kwh = 0.0#in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float(yearly_deemed_loss_kwh))/(jharkhand_constant*24*days_elapsed))*100 #in admin.py file
	yearly_grid_outage_loss_kwh = 0.0 #in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float(yearly_grid_outage_loss_kwh))/(jharkhand_constant*24*days_elapsed))*100 #in admin.py file
	yearly_bd_loss_kwh = 0.0 #in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float(yearly_bd_loss_kwh))/(jharkhand_constant*24*days_elapsed))*100 #in admin.py file
	yearly_dust_loss_kwh = 0.0 #in admin.py file
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float(yearly_dust_loss_kwh))/(jharkhand_constant*24*days_elapsed))*100 #in admin.py file
	yearly_misc_loss =yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf
	#in admin.py file

	j = Jharkhand_Sheet(date=today1,
					  days_elapsed= days_elapsed,
					  daily_target_generation=today_target_generation_value,
					  daily_actual_generation=today_actual_generation_value,
					  irradiation_target_plf=0.0,
					  kwh_target_plf=0.0,
					  monthly_target_generation=monthly_target_generation_value,
					  monthly_actual_generation=monthly_actual_generation_value,
					  yearly_target_generation=yearly_target_generation_value,
					  yearly_actual_generation=yearly_actual_generation_value,
					  daily_target_plf=today_target_plf,
					  daily_actual_plf=today_actual_plf,
					  monthly_target_plf=monthly_target_plf,
					  monthly_actual_plf=monthly_actual_plf,
					  yearly_target_plf=yearly_target_plf,
					  yearly_actual_plf=yearly_actual_plf,
					  daily_target_performance_ratio=today_target_performace_ratio,
					  daily_actual_performance_ratio=today_actual_performance_ratio,
					  monthly_target_performance_ratio=monthly_target_performance_ratio,
					  monthly_actual_performance_ratio=monthly_actual_performance_ratio,
					  yearly_target_performance_ratio=yearly_target_performance_ratio,
					  yearly_actual_performance_ratio=yearly_actual_performance_ratio,
					  daily_target_irradiance=today_target_irradiance,
					  daily_actual_irradiance=today_actual_irradiance,
					  monthly_target_irradiance=monthly_target_irradiance,
					  monthly_actual_irradiance=monthly_actual_irradiance,
					  yearly_target_irradiance=yearly_target_irradiance,
					  yearly_actual_irradiance=yearly_actual_irradiance,
					  daily_irradiance_loss=today_irradiance_loss,
					  monthly_irradiance_loss=monthly_irradiance_loss,
					  yearly_irradiance_loss=yearly_irradiance_loss,
					  daily_deemed_loss=0.00,
					  monthly_deemed_loss=0.00,
					  yearly_deemed_loss=0.00,
					  daily_deemed_loss_plf=today_deemed_loss_plf,
					  monthly_deemed_loss_plf=monthly_deemed_loss_plf,
					  yearly_deemed_loss_plf=yearly_deemed_loss_plf,
					  daily_grid_loss=0.00,
					  monthly_grid_loss=0.00,
					  yearly_grid_loss=0.00,
					  daily_grid_loss_plf=today_grid_outage_loss_plf,
					  monthly_grid_loss_plf=monthly_grid_outage_loss_plf,
					  yearly_grid_loss_plf=yearly_grid_outage_loss_plf,
					  daily_bd_loss=0.00,
					  monthly_bd_loss=0.00,
					  yearly_bd_loss=0.00,
					  daily_bd_loss_plf=today_bd_loss_plf,
					  monthly_bd_loss_plf=monthly_bd_loss_plf,
					  yearly_bd_loss_plf=yearly_bd_loss_plf,
					  daily_dust_loss=0.00,
					  monthly_dust_loss=0.00,
					  yearly_dust_loss=0.00,
					  daily_dust_loss_plf=today_dust_loss_plf,
					  monthly_dust_loss_plf=monthly_dust_loss_plf,
					  yearly_dust_loss_plf=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	j.save()

p_rows, p_cols = siteP.shape
b_rows, b_cols = siteB.shape
j_rows, j_cols = siteJ.shape
c_rows, c_cols = siteC.shape
r_rows, r_cols = siteR.shape

wc_rows, wc_cols = wmsC.shape
wj_rows, wj_cols = wmsJ.shape
wp_rows, wp_cols = wmsP.shape
wr_rows, wr_cols = wmsR.shape

# calculate_panipat_values() # -- DONE
# calculate_castamet_values() # -- DONE
# calculate_beawar_values()	# -- DONE
# calculate_roorkee_values() # -- DONE
# calculate_jharkhand_values()	# -- DONE

def error_page(request):
	return render(request, 'FileSaver/404.html')


#For showing live statistics on a daily basis
def dailyupdates(request):
	lastJrecord = Jharkhand_Sheet.objects.latest('date')
	lastPrecord = Panipat_Sheet.objects.latest('date')
	lastCrecord = Castamet_Sheet.objects.latest('date')
	lastBrecord = Beawar_Sheet.objects.latest('date')
	lastRrecord = Roorkee_Sheet.objects.latest('date')
	global p_rows, b_rows, j_rows, c_rows, r_rows
	global siteP, siteJ, siteR, siteC, siteB, wmsC, wmsJ, wmsP, wmsR


	#prepare lists for data-values

	daily_panipat_gen = []
	daily_jharkhand_gen = []
	daily_castamet_gen = []
	daily_beawar_gen = [siteB[0][3], siteB[1][3], siteB[2][3]]
	# daily_beawar_gen = [siteB[0][date_day], siteB[1][date_day], siteB[2][date_day]]
	daily_roorkee_gen = []

	# for i in range(p_rows):
	# for i in range(22):	actual count
	for i in range(17):		#just for testing
		daily_panipat_gen.append(siteP[i][4])

	# for i in range(j_rows):
	# for i in range(21):	actual count
	for i in range(21):		#just for testing
		daily_jharkhand_gen.append(siteJ[i][4])

	# for i in range(c_rows):
	# for i in range(18):	actual count
	for i in range(22):		#just for testing
		daily_castamet_gen.append(siteC[i][4])

	# for i in range(r_rows):
	# for i in range(21):
	for i in range(14):
		daily_roorkee_gen.append(siteR[i][4])

	context = {
		# 'pcount': p_rows,	#Panipat has 22 invertors
		# 'bcount': 3,		#Beawar has 3 invertors
		# 'jcount': j_rows,	#Jharkhand has 21 invertors
		# 'ccount': c_rows,	#Castamet has 18 invertors
		# 'rcount': r_rows,	#Roorkee has 21 invertors
		'pcount': 22,	#Panipat has 22 invertors
		'bcount': 3,		#Beawar has 3 invertors
		'jcount': 21,	#Jharkhand has 21 invertors
		'ccount': 18,	#Castamet has 18 invertors
		'rcount': 21,	#Roorkee has 21 invertors
		'panipat_object': lastPrecord,
		'jharkhand_object': lastJrecord,
		'castamet_object': lastCrecord,
		'beawar_object': lastBrecord,
		'roorkee_object': lastRrecord,
		'sitePanipat': siteP,
		'siteJharkhand': siteJ,
		'siteRoorkee': siteR,
		'siteCastamet': siteC,
		'siteBeawar': siteB,
		'panipat_gen': daily_panipat_gen,
		'jharkhand_gen': daily_jharkhand_gen,
		'castamet_gen': daily_castamet_gen,
		'roorkee_gen': daily_roorkee_gen,
		'beawar_gen': daily_beawar_gen,
	}
	return render(request, 'FileSaver/statistics.html', context)

#For documentation html page
def startdoc(request):
	return render(request, 'FileSaver/doc.html')

#For HTML page with analysis window
def analysis(request):
	return render(request, 'FileSaver/analysis.html')

#For page with exception report
def report(request):
	lastJrecord = Jharkhand_Sheet.objects.latest('date')
	lastPrecord = Panipat_Sheet.objects.latest('date')
	lastCrecord = Castamet_Sheet.objects.latest('date')
	lastBrecord = Beawar_Sheet.objects.latest('date')
	lastRrecord = Roorkee_Sheet.objects.latest('date')
	prDiffPanipat = lastPrecord.daily_target_performance_ratio - lastPrecord.daily_actual_performance_ratio
	prDiffJharkhand = lastJrecord.daily_target_performance_ratio - lastJrecord.daily_actual_performance_ratio
	prDiffRoorkee = lastRrecord.daily_target_performance_ratio - lastRrecord.daily_actual_performance_ratio
	prDiffCastamet = lastCrecord.daily_target_performance_ratio - lastCrecord.daily_actual_performance_ratio
	prDiffBeawar = lastBrecord.daily_target_performance_ratio - lastBrecord.daily_actual_performance_ratio
	misclossB = (float(lastBrecord.daily_misc_loss)*24)/float(lastBrecord.daily_actual_irradiance)
	misclossP = (float(lastPrecord.daily_misc_loss)*24)/float(lastPrecord.daily_actual_irradiance)
	misclossR = (float(lastRrecord.daily_misc_loss)*24)/float(lastRrecord.daily_actual_irradiance)
	misclossJ = (float(lastJrecord.daily_misc_loss)*24)/float(lastJrecord.daily_actual_irradiance)
	misclossC = (float(lastCrecord.daily_misc_loss)*24)/float(lastCrecord.daily_actual_irradiance)

	context = {
		'panipat_object': lastPrecord,
		'jharkhand_object': lastJrecord,
		'castamet_object': lastCrecord,
		'beawar_object': lastBrecord,
		'roorkee_object': lastRrecord,
		'prDiffP': prDiffPanipat,
		'prDiffJ': prDiffJharkhand,
		'prDiffR': prDiffRoorkee,
		'prDiffC': prDiffCastamet,
		'prDiffB': prDiffBeawar,
		'misclossB': misclossB,
		'misclossP': misclossP,
		'misclossR': misclossR,
		'misclossJ': misclossJ,
		'misclossC': misclossC,
	}
	return render(request, 'FileSaver/exceptionreport.html', context)


#Function for storing the CSV formatted data and then downloading it onto the machine
def downloadreport(request):
	#function for preparing CSV and then download
	return render(request, 'FileSaver/exceptionreport.html')
