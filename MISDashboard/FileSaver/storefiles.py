import os
from datetime import date
import pandas as pd

#sheet variables
site1 = None
site2 = None
site3 = None
site4 = None

#remember to Nullify the sitedatesheet values
today = date.today().strftime('%d-%m-%Y')
path = os.getcwd() + "\..\..\SiteSheets\\" + today
os.chdir(path)

folderlist = [str(i) for i in os.listdir(path='.')]
path_to_folder = None

i=0
#iterate over the 4 folders for 4 sites
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
		else:
			site4 = pd.read_excel(path, skiprows=3)
			i += 1
			print(site4)
		path = os.getcwd() + "\..\\"
		os.chdir(path)