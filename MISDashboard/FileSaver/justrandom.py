import os
from pathlib import Path
from os import path
from datetime import date

today = date.today().strftime('%d-%m-%Y')
print(today)

path = os.getcwd()+"\..\..\SiteSheets"
os.chdir(path)
print(os.getcwd())
# os.mkdir(today)