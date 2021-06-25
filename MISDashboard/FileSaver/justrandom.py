from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

username = 'admin'
password = 'enter@SC21'

user = authenticate(username, password)


#Open the Django database
#Write the 