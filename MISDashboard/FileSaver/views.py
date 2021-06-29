import os
import email
import imaplib
import webbrowser
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

	#select top 4 messages to download each day
	N = 1

	today = date.today().strftime('%d-%m-%Y')
	print(today)

	#search for the SiteSheets folder in the MIS project
	path = os.getcwd()+"\..\..\SiteSheets"
	os.chdir(path)
	os.mkdir(today)			#move to the SiteSheets foler

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
# 1. Collecting the CSV data of four sheets in different variables.
# 2. Declutter all the data from those variables, just keeping only data-containing cells.
# 3. Then, the function for preparing the combined data sheet in the required format.
# 4. Function for storing that in Django database. [includes authentication, automation of Session cookie]
# 5. Function to pass the data from the final-sheet(s) onto the webpage.
# 6. Batch file for automating downloads.