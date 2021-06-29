#This script is made for downloading the email-attachments sent and storing them in the folder.
import os
import email
import imaplib
import webbrowser
from datetime import date

from django.conf import settings
from FileSaver.views import download_files

from email.header import decode_header

download_files()