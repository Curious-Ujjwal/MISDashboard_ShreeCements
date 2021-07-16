import os
import email
import imaplib
import webbrowser
import pandas as pd
from datetime import date
from email.header import decode_header
from django.contrib.auth import login, authenticate
import numpy

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
# 2. Code the calculations part for our Final Sheet 
# 3. Function to pass the data from the final-sheet(s) onto the webpage.
# 4. Batch file for automating downloads.

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

#plant constants
beawar_constant = 62
panipat_constant = 1247.4
roorkee_constant = 999.4
jharkhand_constant = 1998.8
castamet_constant = 999.37

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

	calculate_panipat_values()
	calculate_castamet_values()
	calculate_beawar_values()
	calculate_roorkee_values()
	calculate_jharkhand_values()

	# return 
	pass

#Day and month from date
today = date.today().strftime('%d-%m-%Y')
date_day = int(today[:2])
date_month = int(today[3:5])
date_year = int(today[6:])
days_in_the_year = None

def calculate_days(date_year):
	if (date_year%4) == 0:
		if (date_year%100) == 0:
			if(date_year%400) == 0:
				days_in_the_year = 366
			else:
				days_in_the_year = 365
		else:
			days_in_the_year = 366
	else:
		days_in_the_year = 365

#write the function for days_elapsed after the starting date of the year
days_elapsed = days_in_the_year

#Data used for calculating seasonal tilt
#Admin can modify panipat_global_inclide for any excpected changes

#make a .py file of these constants and import these at the starting of views
#so that everydaythe calculation time is not consumed for report updation
panipat1_global_inclide = [164, 178, 210, 208, 213, 185, 164, 162, 174, 194, 183, 172]
panipat2_global_inclide = [118, 140, 187, 203, 213, 186, 166, 162, 165, 162, 132, 117]
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
panipat1_constant_list = [0.944530409437306, 0.9529803175127, 0.954555380136122, 0.954300017174192, 0.953091560307309, 0.947753511668245, 0.939540661806116, 0.938834687371429, 0.945421487506378, 0.950208497025997, 0.965168644285554, 0.946435450279757]
panipat1_constant_list = [0.921754941158239, 0.9393848287515, 0.948137771519821, 0.952435617251985, 0.952208331023773, 0.947311474902127, 0.939029505439681, 0.937779478459364, 0.941581090707797, 0.939360736441002, 0.930310436479281, 0.920679618774834]
panipat1_seasonal_tilt = [0]*12
panipat2_seasonal_tilt = [0]*12


for i in range(12):
	 if i==1 and days_in_the_year==366:
		panipat1_seasonal_tilt[i] = ((panipat1_global_inclide[i]*panipat1_constant_list[i])/month_days[i]+1)
	else:
		panipat1_seasonal_tilt[i] = ((panipat1_global_inclide[i]*panipat1_constant_list[i])/month_days[i])


for i in range(12):
	if i==1 and days_in_the_year==366:
		panipat2_seasonal_tilt[i] = ((panipat2_global_inclide[i]*panipat2_constant_list[i])/month_days[i]+1)
	else:
		panipat2_seasonal_tilt[i] = ((panipat2_global_inclide[i]*panipat2_constant_list[i])/month_days[i])

#error correction for months of April, May, June
panipat1_seasonal_tilt[3] = 6.23322506140001-0.005
panipat1_seasonal_tilt[4] = panipat_seasonal_tilt[4]-0.31
panipat1_seasonal_tilt[5] = 5.90162280384445+0.01544443


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


castamet_global_inclide = [142.1, 159, 197.7, 209.4, 218.8, 188.4, 168, 159.2, 174.8, 173.8, 136.2, 136.1]
castamet_constant_list = [0.988927347522672, 0.992909399757744, 0.993488062490747, 0.994861378142273, 0.994822772991885, 0.994217824725635, 0.99215753947913, 0.991787606021159, 0.991609222534777, 0.991348933037635, 0.987935230884706, 0.983498304458082]
castamet_5deg_fix_tilt = [0]*12

for i in range(12):
	if i==1 and days_in_the_year==366:
		castamet_5deg_fix_tilt[i] = ((castamet_global_inclide[i]*castamet_constant_list[i])/month_days[i]+1)
	else:
		castamet_5deg_fix_tilt[i] = ((castamet_global_inclide[i]*castamet_constant_list[i])/month_days[i])

#Error correction code for Castamet Site
castamet_5deg_fix_tilt[3] = 6.8158
castamet_5deg_fix_tilt[4] = castamet_5deg_fix_tilt[4] - 0.04
castamet_5deg_fix_tilt[5] = castamet_5deg_fix_tilt[5] - 0.044


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

beawar_seasonal_tilt = [5.55969262291147, 6.37028281140042, 6.307165627972, 6.74832287692192, 6.31875435673262, 6.68, 4.88754635479502, 4.54857603854664, 5.08638962577947, 5.91604603230079, 5.28697120607801, 5.47857152158707]

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


roorkee_global_inclide = [163.9, 179.2, 213.2, 201.4, 210.3, 182.1, 157.7, 159.8, 154.1, 206.8, 200.5, 185.6]
roorkee_constant_list = [0.944395938091124, 0.953324713401739, 0.955421528486887, 0.953051798460278, 0.952698901631499, 0.947261197993877, 0.937324869114803, 0.93845701311761, 0.938736592192122, 0.953461313791492, 0.954948746043538, 0.950556500465678]
roorkee_seasonal_tilt = [0]*12

for i in range(12):
	if i==1 and days_in_the_year==366:
		#in case of month of February in leap year
		roorkee_seasonal_tilt[i] = ((roorkee_global_inclide[i]*roorkee_constant_list[i])/month_days[i]+1)
	else:
		roorkee_seasonal_tilt[i] = ((roorkee_global_inclide[i]*roorkee_constant_list[i])/month_days[i])

roorkee_seasonal_tilt[3] = 5.85394388888889
roorkee_seasonal_tilt[4] = roorkee_seasonal_tilt[4] - 0.075
roorkee_seasonal_tilt[5] = 6.09094888888889 - 0.36


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


jharkhand_seasonal_inclide = [178.4, 178.9, 199.5, 196.1, 206.6, 162.5, 138.2, 139.7, 141.8, 163.7, 175.3, 187.3]
jharkhand_constant_list = [0.947579317979094, 0.951919311027177, 0.951144680217931, 0.951027938381949, 0.951741209093958, 0.941209819176676, 0.928920938728215, 0.929843421973975, 0.933312340425954, 0.940681159048405, 0.947492377629911, 0.950074901876732]
jharkhand_seasonal_tilt = [0]*12

for i in range(12):
	if i==1 and days_in_the_year==366:
		#in case of month of February in leap year
		jharkhand_seasonal_tilt[i] = ((jharkhand_seasonal_inclide[i]*jharkhand_constant_list[i])/month_days[i]+1)
	else:
		jharkhand_seasonal_tilt[i] = ((jharkhand_seasonal_inclide[i]*jharkhand_constant_list[i])/month_days[i])

jharkhand_seasonal_tilt[4] = 5.89235449729202+0.04
jharkhand_seasonal_tilt[5] = 4.70571811653336+0.0205

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