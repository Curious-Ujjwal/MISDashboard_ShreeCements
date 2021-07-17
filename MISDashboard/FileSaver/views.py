import os
import email
import imaplib
import webbrowser
import pandas as pd
from datetime import date
from email.header import decode_header
from django.contrib.auth import login, authenticate
import numpy
from defineconstants import *
from .models import *


#account credentials
username = 'ujjwalrustagi@gmail.com'
password = 'Ujjwal@123'

#function to create the folder name
def clean(text):
	return "".join(c if c.isalnum() else "_" for c in text)

# Create your views here.
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

#Functions to be coded in views:
# Files have been downloaded, so I should not make any double copy by storing them in database.
# Functions that I should focus on:
# 1. Prepare the model for the final sheet first -- DONE
# 2. Code the calculations part for our Final Sheet -- DONE
# 3. Function to pass the data from the final-sheet(s) onto the webpage.
# 4. Batch file for automating downloads. -- DONE

#Site sheet and WMS sheet variables
site1 = None 
site2 = None
site3 = None
site4 = None
site5 = None

wmsC = None
wmsJ = None
wmsP = None
wmsR = None
#remember to Nullify the sitedatesheet values

def sheet_variables():
	today = date.today().strftime('%d-%m-%Y')
	path = os.getcwd() + "\..\..\SiteSheets\\" + today
	os.chdir(path)
	
	folderlist = [str(i) for i in os.listdir(path='.')]
	path_to_folder = None
	
	i=0
	#iterate over the 5 folders for 5 sites
	#and then iterate ovr the 4 folders for 4 WMS reports and 
	#beawar WMS parameters are included in its own report

	for folder in folderlist:
		if folder is not None:
			path = os.getcwd() + "\\" + folder
			os.chdir(path)
			filelist = [str(file) for file in os.listdir(path='.')]
			file = filelist[0]
			path = os.getcwd() + "\\" + file

			if(i == 0):
				site1 = pd.read_excel(path, skiprows=3)
				i += 1
				print(site1)
			elif(i == 1):
				site2 = pd.read_excel(path, skiprows=3)
				i += 1
				print(site2)
			elif(i == 2):
				site3 = pd.read_excel(path, skiprows=3)
				i += 1
				print(site3)
			elif(i == 3):
				site4 = pd.read_excel(path, skiprows=3)
				i+=1
				print(site4)
			elif(i == 4):
				wmsC = pd.read_excel(path, skiprows=3)
				i+=1
				print(wmsC)
			elif(i == 5):
				wmsJ = pd.read_excel(path, skiprows=3)
				i+=1
				print(wmsJ)
			elif(i == 6):
				wmsP = pd.read_excel(path, skiprows=3)
				i+=1
				print(wmsP)
			else:
				wmsR = pd.read_excel(path, skiprows=3)
				i += 1
				print(wmsR)
			path = os.getcwd() + "\..\\"
			os.chdir(path)



def calculate_values():
	site1 = site1.to_numpy()
	site2 = site2.to_numpy()
	site3 = site3.to_numpy()
	site4 = site4.to_numpy()
	site5 = site5.to_numpy()

	wmsC = wmsC.to_numpy()
	wmsJ = wmsJ.to_numpy()
	wmsP = wmsP.to_numpy()
	wmsR = wmsR.to_numpy()

	#these functions are called to save the latest data in the database
	calculate_panipat_values()
	calculate_castamet_values()
	calculate_beawar_values()
	calculate_roorkee_values()
	calculate_jharkhand_values()

	#then make a call to open the dashboard main page instead of pass statement
	pass

#return the no. of days in a year based on if it is a leap/non-leap year
# true -> leap year
# false -> non-leap year
def calculate_days(date_year):
	if (date_year%4) == 0:
		if (date_year%100) == 0:
			if(date_year%400) == 0:
				return true
			else:
				return false
		else:
			return true
	else:
		return false

#Day and month from date
today = date.today().strftime('%d-%m-%Y')
date_day = int(today[:2])
date_month = int(today[3:5])
date_year = int(today[6:])
days_in_the_year = 366 if calculate_days(date_year) else 365

#write the function for days_elapsed after the starting date of the year
days_elapsed = days_in_the_year

#Data used for calculating seasonal tilt
#Admin can modify panipat_global_inclide for any excpected changes
panipat1_seasonal_tilt = None
panipat2_seasonal_tilt = None
roorkee_seasonal_tilt = None
jharkhand_seasonal_tilt = None
castamet_5deg_fix_tilt = None
beawar_seasonal_tilt = b_beawar_seasonal_tilt

if(calculate(date_year)):
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


def calculate_panipat_values():
	#Daily parameters calculation
	today_target_generation_value = int(100)	#this value is entered by user?
	today_actual_generation_value = 100	#add all the values of generation from all the invertors
	today_target_plf = (((float)today_target_generation_value)/(panipat_constant*24))*100
	today_actual_plf = (((float)today_actual_generation_value)/(panipat_constant*24))*100
	today_target_irradiance = (panipat1_seasonal_tilt[date_month]*999.4 + panipat2_seasonal_tilt[date_month]*248)/panipat_constant
	today_actual_irradiance = float(100)	#to be taken as an input from user
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*panipat_constant))*100
	today_actual_performance_ratio = ((float(today_actual_generation_value))/(today_actual_irradiance*panipat_constant))*100
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = float(0)	#given by the user
	today_deemed_loss_plf = (((float)today_deemed_loss_kwh)/(panipat_constant*24))*100
	today_grid_outage_loss_kwh = float(0)	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(panipat_constant*24))*100
	today_bd_loss_kwh = float(0)	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(panipat_constant*24))*100
	today_dust_loss_kwh = float(0) #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(panipat_constant*24))*100
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly parameter values
	monthly_target_generation_value = today_target_generation_value*date_day + 0 #DOUBT
	monthly_actual_generation_value = 100 + 0 #take sum of the previously stored and current values of all the invertors
	monthly_target_plf = (((float)monthly_target_generation_value)/(panipat_constant*24*date_day))*100
	monthly_actual_plf = (((float)monthly_actual_generation_value)/(panipat_constant*24*date_day))*100
	monthly_target_irradiance = 1.0 #maybe fixed value for fixed parameters DOUBT
	monthly_actual_irradiance = float(100)	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*panipat_constant))*100
	monthly_actual_performance_ratio = ((float(monthly_actual_generation_value))/(monthly_target_irradiance*panipat_constant))*100
	monthly_irradiance_loss = monthly_target_plf-0	#the '0' value is calculated by taking average after taking today_irradiance_loss as input
	monthly_deemed_loss_kwh = float(0)	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh
	monthly_deemed_loss_plf = (((float)monthly_deemed_loss_kwh)/(panipat_constant*24*date_day))*100
	monthly_grid_outage_loss_kwh = float(0)	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh
	monthly_grid_outage_loss_plf = (((float)monthly_grid_outage_loss_kwh)/(panipat_constant*24*date_day))*100
	monthly_bd_loss_kwh = float(0)	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh
	monthly_bd_loss_plf = (((float)monthly_bd_loss_kwh)/(panipat_constant*24*date_day))*100
	monthly_dust_loss_kwh = float(0)	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh
	monthly_dust_loss_plf = (((float)monthly_dust_loss_kwh)/(panipat_constant*24*date_day))*100
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = int(0)		#sum of all monthly_target_generation_value
	yearly_actual_generation_value = int(0)		#sum of all monthly_actual_generation_value
	yearly_target_plf = (((float)yearly_target_generation_value)/(panipat_constant*24*days_elapsed))*100
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = (((float)yearly_actual_generation_value)/(panipat_constant*24*days_elapsed))*100
	sumall = 100	
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = (sumall/(float)days_elapsed)
	avg1 = None		#average of all the seaasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt1
	avg2 = None		#average of all the seasonal tilts from the year_start_month to the current_month from panipat_seasonal_tilt2
	yearly_target_irradiance = (avg1*999.4 + avg2*248)/panipat_constant
	yearly_target_performance_ratio = ((float)yearly_target_generation_value/(panipat_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = ((float)yearly_actual_generation_value/(panipat_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf
	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	gen = None
	yearly_irradiance_loss = ((float)yearly_target_generation_value/(panipat_constant*24*days_elapsed))*100 - ((float)gen/(castamet_constant*24*days_elapsed))*100
	yearly_deemed_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float)yearly_deemed_loss_kwh/(panipat_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float)yearly_grid_outage_loss_kwh/(panipat_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float)yearly_bd_loss_kwh/(panipat_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float)yearly_dust_loss_kwh/(panipat_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf

	p = Panipat_Sheet(date=today, 
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
					  daily_deemed_loss=today_deemed_loss_plf,
					  monthly_deemed_loss=monthly_deemed_loss_plf,
					  yearly_deemed_loss=yearly_deemed_loss_plf,
					  daily_grid_loss=today_grid_outage_loss_plf,
					  monthly_grid_loss=monthly_grid_outage_loss_plf,
					  yearly_grid_loss=yearly_grid_outage_loss_plf,
					  daily_bd_loss=today_bd_loss_plf,
					  monthly_bd_loss=monthly_bd_loss_plf,
					  yearly_bd_loss=yearly_bd_loss_plf,
					  daily_dust_loss=today_dust_loss_plf,
					  monthly_dust_los=monthly_dust_loss_plf,
					  yearly_dust_loss=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	p.save()


def calculate_castamet_values():
	#Daily parameter values
	today_target_generation_value = int(100)	#this value is entered by user?
	today_actual_generation_value = 100			#add all the values of generation from all the invertors
	today_target_plf = (((float)today_target_generation_value)/(castamet_constant*24))*100
	today_actual_plf = (((float)today_actual_generation_value)/(castamet_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = float(100)	#to be taken as an input from user oR from WMS report?
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*castamet_constant))*100
	today_actual_performance_ratio = ((float(today_actual_generation_value))/(today_actual_irradiance*castamet_constant))*100
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = float(0)	#given by the user
	today_deemed_loss_plf = (((float)today_deemed_loss_kwh)/(castamet_constant*24))*100
	today_grid_outage_loss_kwh = float(0)	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(castamet_constant*24))*100
	today_bd_loss_kwh = float(0)	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(castamet_constant*24))*100
	today_dust_loss_kwh = float(0) #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(castamet_constant*24))*100
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day #DOUBT
	monthly_actual_generation_value = 100 + 0 #take sum of the previously stored and current values of all the invertors
	monthly_target_plf = (((float)monthly_target_generation_value)/(castamet_constant*24*date_day))*100
	monthly_actual_plf = (((float)monthly_actual_generation_value)/(castamet_constant*24*date_day))*100
	monthly_target_irradiance = 1.0 #maybe fixed value for fixed parameters DOUBT(daily_target_irradiance)
	monthly_actual_irradiance = float(100)	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*castamet_constant))*100
	monthly_actual_performance_ratio = ((float(monthly_actual_generation_value))/(monthly_actual_irradiance*castamet_constant))*100
	monthly_irradiance_loss = monthly_target_plf-0	#the '0' value is calculated by taking average after taking today_irradiance_loss as input
	monthly_deemed_loss_kwh = float(0)	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh
	monthly_deemed_loss_plf = (((float)monthly_deemed_loss_kwh)/(castamet_constant*24*date_day))*100
	monthly_grid_outage_loss_kwh = float(0)	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh
	monthly_grid_outage_loss_plf = (((float)monthly_grid_outage_loss_kwh)/(castamet_constant*24*date_day))*100
	monthly_bd_loss_kwh = float(0)	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh
	monthly_bd_loss_plf = (((float)monthly_bd_loss_kwh)/(castamet_constant*24*date_day))*100
	monthly_dust_loss_kwh = float(0)	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh
	monthly_dust_loss_plf = (((float)monthly_dust_loss_kwh)/(castamet_constant*24*date_day))*100
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = int(0)		#sum of all monthly_target_generation_value
	yearly_actual_generation_value = int(0)		#sum of all monthly_actual_generation_value
	yearly_target_plf = (((float)yearly_target_generation_value)/(castamet_constant*24*days_elapsed))*100
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = (((float)yearly_actual_generation_value)/(castamet_constant*24*days_elapsed))*100
	sumall = 100	
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = (sumall/(float)days_elapsed)
	avg1 = None		#average of all the 5degfix tilts from the year_start_month to the current_month from castamet_5deg_fix_tilt
	yearly_target_irradiance = avg1
	yearly_target_performance_ratio = ((float)yearly_target_generation_value/(castamet_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = ((float)yearly_actual_generation_value/(castamet_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	yearly_irradiance_loss = ((float)yearly_target_generation_value/(castamet_constant*24*days_elapsed))*100 - ((float)gen/(castamet_constant*24*days_elapsed))*100
	yearly_deemed_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float)yearly_deemed_loss_kwh/(castamet_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float)yearly_grid_outage_loss_kwh/(castamet_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float)yearly_bd_loss_kwh/(castamet_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float)yearly_dust_loss_kwh/(castamet_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf

	c = Castamet_Sheet(date=today, 
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
					  daily_deemed_loss=today_deemed_loss_plf,
					  monthly_deemed_loss=monthly_deemed_loss_plf,
					  yearly_deemed_loss=yearly_deemed_loss_plf,
					  daily_grid_loss=today_grid_outage_loss_plf,
					  monthly_grid_loss=monthly_grid_outage_loss_plf,
					  yearly_grid_loss=yearly_grid_outage_loss_plf,
					  daily_bd_loss=today_bd_loss_plf,
					  monthly_bd_loss=monthly_bd_loss_plf,
					  yearly_bd_loss=yearly_bd_loss_plf,
					  daily_dust_loss=today_dust_loss_plf,
					  monthly_dust_los=monthly_dust_loss_plf,
					  yearly_dust_loss=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	c.save()


def calculate_beawar_values():
	#Daily parameter values
	today_target_generation_value = int(100)	#this value is entered by user?
	today_actual_generation_value = 100			#take the value of Actual Solar Gen from Beawar SieSheet
	today_target_plf = (((float)today_target_generation_value)/(beawar_constant*24))*100
	today_actual_plf = (((float)today_actual_generation_value)/(beawar_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = float(100)	#take the value of Actual Irradiance of that date
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*beawar_constant))*100
	today_actual_performance_ratio = ((float(today_actual_generation_value))/(today_actual_irradiance*beawar_constant))*100
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation from the Beawar Sheet)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = float(0)	#given by the user
	today_deemed_loss_plf = (((float)today_deemed_loss_kwh)/(castamet_constant*24))*100
	today_grid_outage_loss_kwh = float(0)	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(castamet_constant*24))*100
	today_bd_loss_kwh = float(0)	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(castamet_constant*24))*100
	today_dust_loss_kwh = float(0) #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(castamet_constant*24))*100
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day #DOUBT
	monthly_actual_generation_value = 100 #take sum of the previously stored and current values of the Actual Solar Gen
	monthly_target_plf = (((float)monthly_target_generation_value)/(beawar_constant*24*date_day))*100
	monthly_actual_plf = (((float)monthly_actual_generation_value)/(beawar_constant*24*date_day))*100
	monthly_target_irradiance = daily_target_irradiance
	monthly_actual_irradiance = float(100)	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*beawar_constant))*100
	monthly_actual_performance_ratio = ((float(monthly_actual_generation_value))/(monthly_actual_irradiance*beawar_constant))*100
	monthly_irradiance_loss = monthly_target_plf-0	#the '0' value is calculated by taking average of the prev. stored monthly_irradiance_loss and today's Target PLF based on Actual Irradiation
	monthly_deemed_loss_kwh = float(0)	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh
	monthly_deemed_loss_plf = (((float)monthly_deemed_loss_kwh)/(beawar_constant*24*date_day))*100
	monthly_grid_outage_loss_kwh = float(0)	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh
	monthly_grid_outage_loss_plf = (((float)monthly_grid_outage_loss_kwh)/(beawar_constant*24*date_day))*100
	monthly_bd_loss_kwh = float(0)	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh + sum of today_external_loss & prev. calculated monthly_external_loss
	monthly_bd_loss_plf = (((float)monthly_bd_loss_kwh)/(beawar_constant*24*date_day))*100
	monthly_dust_loss_kwh = float(0)	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh
	monthly_dust_loss_plf = (((float)monthly_dust_loss_kwh)/(beawar_constant*24*date_day))*100
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = int(0)		#sum of all monthly_target_generation_value OR sum of prev. stored yearly_target_generation_value + today_generation_value
	yearly_actual_generation_value = int(0)		#sum of all monthly_actual_generation_value OR sum of prev. stored yearly_target_generation_value + today_generation_value
	yearly_target_plf = (((float)yearly_target_generation_value)/(beawar_constant*24*days_elapsed))*100
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = (((float)yearly_actual_generation_value)/(beawar_constant*24*days_elapsed))*100
	sumall = 100	
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = (sumall/(float)days_elapsed) + 0.1
	avg1 = None		#average of all the beawar_seasonal_tilt(s) from the year_start_month to the current_month from castamet_5deg_fix_tilt
	yearly_target_irradiance = avg1 + 0.15
	yearly_target_performance_ratio = ((float)yearly_target_generation_value/(beawar_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = ((float)yearly_actual_generation_value/(beawar_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	gen = None
	yearly_irradiance_loss = ((float)yearly_target_generation_value/(beawar_constant*24*days_elapsed))*100 - ((float)gen/(beawar_constant*24*days_elapsed))*100
	yearly_deemed_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float)yearly_deemed_loss_kwh/(beawar_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float)yearly_grid_outage_loss_kwh/(beawar_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh  + monthly_exteernal_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float)yearly_bd_loss_kwh/(beawar_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float)yearly_dust_loss_kwh/(beawar_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf

	b = Beawar_Sheet(date=today, 
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
					  daily_deemed_loss=today_deemed_loss_plf,
					  monthly_deemed_loss=monthly_deemed_loss_plf,
					  yearly_deemed_loss=yearly_deemed_loss_plf,
					  daily_grid_loss=today_grid_outage_loss_plf,
					  monthly_grid_loss=monthly_grid_outage_loss_plf,
					  yearly_grid_loss=yearly_grid_outage_loss_plf,
					  daily_bd_loss=today_bd_loss_plf,
					  monthly_bd_loss=monthly_bd_loss_plf,
					  yearly_bd_loss=yearly_bd_loss_plf,
					  daily_dust_loss=today_dust_loss_plf,
					  monthly_dust_los=monthly_dust_loss_plf,
					  yearly_dust_loss=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	b.save()

def calculate_roorkee_values():
	#Daily parameter values
	today_target_generation_value = int(100)	#this value is entered by user?
	today_actual_generation_value = 100			#add all the values of generation from all the invertors
	today_target_plf = (((float)today_target_generation_value)/(roorkee_constant*24))*100
	today_actual_plf = (((float)today_actual_generation_value)/(roorkee_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = float(100)	#to be taken as an input from user oR from WMS report? convet from W/m^2 to kWh/m^2
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*roorkee_constant))*100
	today_actual_performance_ratio = ((float(today_actual_generation_value))/(today_actual_irradiance*roorkee_constant))*100
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = float(0)	#given by the user
	today_deemed_loss_plf = (((float)today_deemed_loss_kwh)/(roorkee_constant*24))*100
	today_grid_outage_loss_kwh = float(0)	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(roorkee_constant*24))*100
	today_bd_loss_kwh = float(0)	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(roorkee_constant*24))*100
	today_dust_loss_kwh = float(0) #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(roorkee_constant*24))*100
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day #DOUBT
	monthly_actual_generation_value = 100 + 0 #take sum of the previously stored and current values of all the invertors
	monthly_target_plf = (((float)monthly_target_generation_value)/(roorkee_constant*24*date_day))*100
	monthly_actual_plf = (((float)monthly_actual_generation_value)/(roorkee_constant*24*date_day))*100
	monthly_target_irradiance = daily_target_irradiance
	monthly_actual_irradiance = float(100)	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*roorkee_constant))*100
	monthly_actual_performance_ratio = ((float(monthly_actual_generation_value))/(monthly_actual_irradiance*roorkee_constant))*100
	monthly_irradiance_loss = monthly_target_plf-0	#the '0' value is calculated by taking average after taking today_irradiance_loss as input
	monthly_deemed_loss_kwh = float(0)	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh
	monthly_deemed_loss_plf = (((float)monthly_deemed_loss_kwh)/(roorkee_constant*24*date_day))*100
	monthly_grid_outage_loss_kwh = float(0)	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh
	monthly_grid_outage_loss_plf = (((float)monthly_grid_outage_loss_kwh)/(roorkee_constant*24*date_day))*100
	monthly_bd_loss_kwh = float(0)	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh
	monthly_bd_loss_plf = (((float)monthly_bd_loss_kwh)/(roorkee_constant*24*date_day))*100
	monthly_dust_loss_kwh = float(0)	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh
	monthly_dust_loss_plf = (((float)monthly_dust_loss_kwh)/(roorkee_constant*24*date_day))*100
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = int(0)		#sum of all monthly_target_generation_value
	yearly_actual_generation_value = int(0)		#sum of all monthly_actual_generation_value
	yearly_target_plf = (((float)yearly_target_generation_value)/(roorkee_constant*24*days_elapsed))*100
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = (((float)yearly_actual_generation_value)/(roorkee_constant*24*days_elapsed))*100
	sumall = 100	
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = (sumall/(float)days_elapsed)
	avg1 = None		#average of all the roorkee_seasonal_tilts from the year_start_month to the current_month from castamet_5deg_fix_tilt
	yearly_target_irradiance = avg1
	yearly_target_performance_ratio = ((float)yearly_target_generation_value/(roorkee_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = ((float)yearly_actual_generation_value/(roorkee_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	yearly_irradiance_loss = ((float)yearly_target_generation_value/(roorkee_constant*24*days_elapsed))*100 - ((float)gen/(castamet_constant*24*days_elapsed))*100
	yearly_deemed_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float)yearly_deemed_loss_kwh/(roorkee_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float)yearly_grid_outage_loss_kwh/(roorkee_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float)yearly_bd_loss_kwh/(roorkee_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float)yearly_dust_loss_kwh/(roorkee_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf

	r = Roorkee_Sheet(date=today, 
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
					  daily_deemed_loss=today_deemed_loss_plf,
					  monthly_deemed_loss=monthly_deemed_loss_plf,
					  yearly_deemed_loss=yearly_deemed_loss_plf,
					  daily_grid_loss=today_grid_outage_loss_plf,
					  monthly_grid_loss=monthly_grid_outage_loss_plf,
					  yearly_grid_loss=yearly_grid_outage_loss_plf,
					  daily_bd_loss=today_bd_loss_plf,
					  monthly_bd_loss=monthly_bd_loss_plf,
					  yearly_bd_loss=yearly_bd_loss_plf,
					  daily_dust_loss=today_dust_loss_plf,
					  monthly_dust_los=monthly_dust_loss_plf,
					  yearly_dust_loss=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	r.save()

def calculate_jharkhand_values():
	#Daily parameter values
	today_target_generation_value = int(100)	#this value is entered by user?
	today_actual_generation_value = 100			#add all the values of generation from all the invertors
	today_target_plf = (((float)today_target_generation_value)/(jharkhand_constant*24))*100
	today_actual_plf = (((float)today_actual_generation_value)/(jharkhand_constant*24))*100
	today_target_irradiance = float(0)		#user entry
	today_actual_irradiance = float(100)	#to be taken as an input from user oR from WMS report? convet from W/m^2 to kWh/m^2
	today_target_performace_ratio = ((float(today_target_generation_value))/(today_target_irradiance*jharkhand_constant))*100
	today_actual_performance_ratio = ((float(today_actual_generation_value))/(today_actual_irradiance*jharkhand_constant))*100
	today_irradiance_loss = today_target_plf - 0 #(value of Target PLF based on Actual Irradiation given by the user)
	today_generation_loss = today_target_plf-today_actual_plf
	today_deemed_loss_kwh = float(0)	#given by the user
	today_deemed_loss_plf = (((float)today_deemed_loss_kwh)/(jharkhand_constant*24))*100
	today_grid_outage_loss_kwh = float(0)	#given by the user
	today_grid_outage_loss_plf = (today_grid_outage_loss_kwh/(jharkhand_constant*24))*100
	today_bd_loss_kwh = float(0)	#given by the user
	today_bd_loss_plf = (today_bd_loss_kwh/(jharkhand_constant*24))*100
	today_dust_loss_kwh = float(0) #given by the user
	today_dust_loss_plf = (today_dust_loss_kwh/(jharkhand_constant*24))*100
	today_misc_loss = today_generation_loss-today_irradiance_loss-today_deemed_loss_plf-today_grid_outage_loss_plf-today_bd_loss_plf-today_dust_loss_plf

	#Monthly paramter values
	monthly_target_generation_value = today_target_generation_value*date_day #DOUBT
	monthly_actual_generation_value = 100 + 0 #take sum of the previously stored and current values of all the invertors
	monthly_target_plf = (((float)monthly_target_generation_value)/(jharkhand_constant*24*date_day))*100
	monthly_actual_plf = (((float)monthly_actual_generation_value)/(jharkhand_constant*24*date_day))*100
	monthly_target_irradiance = daily_target_irradiance
	monthly_actual_irradiance = float(100)	#take avg. of all the values for the current month from WMS sheet and prev. stored monthly_actual_irradiance
	monthly_target_performance_ratio = ((float(monthly_target_generation_value))/(monthly_target_irradiance*jharkhand_constant))*100
	monthly_actual_performance_ratio = ((float(monthly_actual_generation_value))/(monthly_actual_irradiance*jharkhand_constant))*100
	monthly_irradiance_loss = monthly_target_plf-0	#the '0' value is calculated by taking average after taking today_irradiance_loss as input
	monthly_deemed_loss_kwh = float(0)	#sum of today_deemed_loss_kwh & prev. calculated monthly_deemed_loss_kwh
	monthly_deemed_loss_plf = (((float)monthly_deemed_loss_kwh)/(jharkhand_constant*24*date_day))*100
	monthly_grid_outage_loss_kwh = float(0)	#sum of today_grid_outage_loss_kwh & prev. calculated monthly_grid_outage_loss_kwh
	monthly_grid_outage_loss_plf = (((float)monthly_grid_outage_loss_kwh)/(jharkhand_constant*24*date_day))*100
	monthly_bd_loss_kwh = float(0)	#sum of today_bd_loss_kwh & prev. calculated monthly_bd_loss_kwh
	monthly_bd_loss_plf = (((float)monthly_bd_loss_kwh)/(jharkhand_constant*24*date_day))*100
	monthly_dust_loss_kwh = float(0)	#sum of today_dust_loss_kwh + prev. calculated monthly_dust_loss_kwh
	monthly_dust_loss_plf = (((float)monthly_dust_loss_kwh)/(jharkhand_constant*24*date_day))*100
	monthly_generation_loss = monthly_target_plf-monthly_actual_plf
	monthly_misc_loss = monthly_generation_loss-monthly_irradiance_loss-monthly_deemed_loss_plf-monthly_grid_outage_loss_plf-monthly_bd_loss_plf-monthly_dust_loss_plf

	#Yearly parameter values
	yearly_target_generation_value = int(0)		#sum of all monthly_target_generation_value
	yearly_actual_generation_value = int(0)		#sum of all monthly_actual_generation_value
	yearly_target_plf = (((float)yearly_target_generation_value)/(jharkhand_constant*24*days_elapsed))*100
		#calculate the days_elapsed from the given starting date in the year
	yearly_actual_plf = (((float)yearly_actual_generation_value)/(jharkhand_constant*24*days_elapsed))*100
	sumall = 100	
	"""
		Basically sumall contains the weighted sum of all values of the month-end irradiance 
		or the monthly last-day recorded irradiance multiplied with 
		either no. of days or the days_elapsed if it is a current month.
	"""
	yearly_actual_irradiance = (sumall/(float)days_elapsed)
	avg1 = None		#average of all the jharkhand_seasonal_tilts from the year_start_month to the current_month from jharkhand_seasonal_tilt
	yearly_target_irradiance = avg1
	yearly_target_performance_ratio = ((float)yearly_target_generation_value/(jharkhand_constant*yearly_target_irradiance*days_elapsed))*100
	yearly_actual_performance_ratio = ((float)yearly_actual_generation_value/(jharkhand_constant*yearly_actual_irradiance*days_elapsed))*100
	yearly_generation_loss = yearly_target_plf - yearly_actual_plf

	#take input of target_plf_based_on_actual_irradiation parameter -> irradiation_target_plf
	#and then calculate target_plf_based_on_kwh -> kwh_target_plf = (irradiation_target_plf*(constant_of_site)*24)/100
	#then add it to the prev. stored yearly_irradiance_loss and then save it to current, this value is subtracted from the first value
	#let this value be gen for now
	yearly_irradiance_loss = ((float)yearly_target_generation_value/(jharkhand_constant*24*days_elapsed))*100 - ((float)gen/(castamet_constant*24*days_elapsed))*100
	yearly_deemed_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_deemed_loss_plf = ((float)yearly_deemed_loss_kwh/(jharkhand_constant*24*days_elapsed))*100
	yearly_grid_outage_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_deemed_loss_kwh calculated uptill the current day
	"""
	yearly_grid_outage_loss_plf = ((float)yearly_grid_outage_loss_kwh/(jharkhand_constant*24*days_elapsed))*100
	yearly_bd_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_bd_loss_kwh calculated uptill the current day
	"""
	yearly_bd_loss_plf = ((float)yearly_bd_loss_kwh/(jharkhand_constant*24*days_elapsed))*100
	yearly_dust_loss_kwh = sumall
	"""
		Here sumall is basically the sum of all the monthly_dust_loss_kwh calculated uptill the current day
	"""
	yearly_dust_loss_plf = ((float)yearly_dust_loss_kwh/(jharkhand_constant*24*days_elapsed))*100
	yearly_misc_loss = yearly_generation_loss-yearly_irradiance_loss-yearly_deemed_loss_plf-yearly_grid_outage_loss_plf-yearly_bd_loss_plf-yearly_dust_loss_plf

	j = Jharkhand_Sheet(date=today, 
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
					  daily_deemed_loss=today_deemed_loss_plf,
					  monthly_deemed_loss=monthly_deemed_loss_plf,
					  yearly_deemed_loss=yearly_deemed_loss_plf,
					  daily_grid_loss=today_grid_outage_loss_plf,
					  monthly_grid_loss=monthly_grid_outage_loss_plf,
					  yearly_grid_loss=yearly_grid_outage_loss_plf,
					  daily_bd_loss=today_bd_loss_plf,
					  monthly_bd_loss=monthly_bd_loss_plf,
					  yearly_bd_loss=yearly_bd_loss_plf,
					  daily_dust_loss=today_dust_loss_plf,
					  monthly_dust_los=monthly_dust_loss_plf,
					  yearly_dust_loss=yearly_dust_loss_plf,
					  daily_misc_loss=today_misc_loss,
					  monthly_misc_loss=monthly_misc_loss,
					  yearly_misc_loss=yearly_misc_loss
		)
	j.save()