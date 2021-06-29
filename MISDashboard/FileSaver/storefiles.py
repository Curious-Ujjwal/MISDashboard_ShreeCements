#This script is made for storing files/attachments downloaded with the help of
#filedownload.py into the DJANGO database.

import requests	
from bs4 import BeautifulSoup
headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}
with requests.Session() as s:

	#                    -----------------                   
	#                   -!-!-!-!-!-!-!-!-!-                  
	# url needs to be updated after this software is deployed
	#                   -!-!-!-!-!-!-!-!-!-                      
	#                    -----------------                       
	
	url = 'http://localhost:8000/admin/login/?next=/admin/'
	r = s.get(url, headers=headers)
	print(r.content)
	# soup = BeautifulSoup(r.content, 'html5lib')
	# soup.find('input', attrs={''})
	'csrfmiddlewaretoken': 'GewlpLRt1nz6CHxofNZqFUKsjjhe6LEro1DHTnjd73B6CHW8OkWkzP1JWSK1IfHj'
	'username': 'admin'
	'password': 'SCA@2021'
	'next': '/admin/'
