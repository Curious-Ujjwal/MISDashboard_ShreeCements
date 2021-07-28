import numpy
from datetime import date
import pandas as pd
import os

siteP = None 	#site1
siteB = None	#siteB
siteJ = None	#siteJ
siteC = None	#siteC
siteR = None	#siteR

wmsC = None
wmsJ = None
wmsP = None
wmsR = None

def sheet_variables():
	today = date.today().strftime('%d-%m-%Y')
	# path = os.getcwd() + "\..\..\SiteSheets\\" + today
	#Uncomment after debug successful
	# path = os.getcwd() + "\\..\\..\\SiteSheets\\" + '30-06-2021'
	path = os.getcwd() + "\\..\\SiteSheets\\" + '30-06-2021'
	# print('AGAIN')
	os.chdir(path)
	# print('HI')
	# print(os.getcwd())
	# print('HI')
	
	folderlist = [str(i) for i in os.listdir(path='.')]
	# print(folderlist)
	path_to_folder = None
	
	i=0
	#iterate over the 5 folders for 5 sites
	#and then iterate ovr the 4 folders for 4 WMS reports and 
	#beawar WMS parameters are included in its own report

	for folder in folderlist:
		if folder is not None:
			path = os.getcwd() + "\\" + folder
			# print(path)
			os.chdir(path)
			filelist = [str(file) for file in os.listdir(path='.')]
			file = filelist[0]
			path = os.getcwd() + "\\" + file

			if(i == 0):
				global siteP
				siteP = pd.read_excel(path, skiprows=6, engine='openpyxl')
				i += 1
				# print(site1)
			elif(i == 1):
				global siteB
				siteB = pd.read_excel(path, skiprows=2, engine='openpyxl')
				i += 1
				# print(site2)
			elif(i == 2):
				global siteJ
				siteJ = pd.read_excel(path, skiprows=3, engine='openpyxl')
				i += 1
				# print(site3)
			elif(i == 3):
				global siteC
				siteC = pd.read_excel(path, skiprows=6, engine='openpyxl')
				i+=1
				# print(site4)
			elif(i == 4):
				global siteR
				siteR = pd.read_excel(path, skiprows=2, engine='openpyxl')
				#skip 2 rows in reading Beawar Sheet
				i+=1
				# print(site5)
			elif(i == 5):
				global wmsC
				wmsC = pd.read_excel(path, skiprows=3, engine='openpyxl')
				i+=1
				# print(wmsC)	
			elif(i == 6):
				global wmsJ
				wmsJ = pd.read_excel(path, skiprows=3, engine='openpyxl')
				i+=1
				# print(wmsJ)
			elif(i == 7):
				global wmsP
				wmsP = pd.read_excel(path, skiprows=3, engine='openpyxl')
				i+=1
				# print(wmsP)
			elif(i == 8):
				global wmsR
				wmsR = pd.read_excel(path, skiprows=3, engine='openpyxl')
				i += 1
				# print(wmsR)
				path = os.getcwd() + "\\..\\"
				os.chdir(path)
				break
			path = os.getcwd() + "\\..\\"
			os.chdir(path)

	# print(siteP)
	# print(os.getcwd())


def calculate_values():
	global siteP
	siteP = siteP.to_numpy()
	global siteB
	siteB = siteB.to_numpy()
	global siteJ
	siteJ = siteJ.to_numpy()
	global siteC
	siteC = siteC.to_numpy()
	global siteR
	siteR = siteR.to_numpy()

	global wmsC
	wmsC = wmsC.to_numpy()
	global wmsJ
	wmsJ = wmsJ.to_numpy()
	global wmsP
	wmsP = wmsP.to_numpy()
	global wmsR
	wmsR = wmsR.to_numpy()

	#these functions are called to save the latest data in the database
	

	#then make a call to open the dashboard main page instead of pass statement
	pass


sheet_variables()
calculate_values()