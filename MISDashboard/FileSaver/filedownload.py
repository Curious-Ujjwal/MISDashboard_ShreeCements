import imaplib
import email
from email.header import decode_header
import webbrowser
import os

username = 'ujjwalrustagi@gmail.com'
password = 'Ujjwal@123'

def clean(text):
	return "".join(c if c.isalnum() else "_" for c in text)

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)

status, messages = imap.select('INBOX')
N = 4
messages = int(messages[0])

for i in range(messages, messages-N, -1):
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

			print("Subject:", subject)
			print("From:", From)

			if msg.is_multipart():
				for part in msg.walk():
					content_type = part.get_content_type()
					content_disposition = str(part.get("Content-Disposition"))

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

							filepath = os.path.join(folder_name, filename)

							open(filepath, "wb").write(part.get_payload(decode=True))
			else:
				content_type = msg.get_content_type()
				body = msg.get_payload(decode=True).decode()

				if content_type == "text/plain":
					print(body)

			if content_type == "text/html":
				folder_name = clean(subject)
				if not os.path.isdir(folder_name):
					os.mkdir(folder_name)

				filename = "index.html"
				filepath = os.path.join(folder_name, filename)

				open(filepath, "w").write(body)
				webbrowser.open(filepath)
			print("^"*100)


imap.close()
imap.logout()