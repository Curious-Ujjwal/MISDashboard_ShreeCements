import os
import email
import imaplib
import webbrowser
import pandas as pd
from datetime import date
from email.header import decode_header
from django.contrib.auth import login, authenticate

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
# 1. Prepare the model for the final sheet first
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