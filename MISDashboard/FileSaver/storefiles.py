import os
from datetime import date
import pandas as pd

#sheet variables
today = date.today().strftime('%d-%m-%Y')
# path = os.getcwd() + "\..\..\SiteSheets\\" + today
path = os.getcwd() + "\..\..\SiteSheets\\" + '30-06-2021'
os.chdir(path)

folderlist = [str(i) for i in os.listdir(path='.')]
path_to_folder = None

i=0
#iterate over the 5 folders for 5 sites
#and then iterate ovr the 4 folders for 4 WMS reports and 
#beawar WMS parameters are included in its own report

siteP = None 
siteB = None
siteJ = None
siteC = None
siteR = None

wmsC = None
wmsJ = None
wmsP = None
wmsR = None

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
			# print(site1)
		elif(i == 1):
			site2 = pd.read_excel(path, skiprows=3)
			i += 1
			# print(site2)
		elif(i == 2):
			site3 = pd.read_excel(path, skiprows=3)
			i += 1
			# print(site3)
		elif(i == 3):
			site4 = pd.read_excel(path, skiprows=3)
			i+=1
			# print(site4)
		elif(i == 4):
			wmsC = pd.read_excel(path, skiprows=3)
			i+=1
			# print(wmsC)
		elif(i == 5):
			wmsJ = pd.read_excel(path, skiprows=3)
			i+=1
			# print(wmsJ)
		elif(i == 6):
			wmsP = pd.read_excel(path, skiprows=3)
			i+=1
			# print(wmsP)
		else:
			wmsR = pd.read_excel(path, skiprows=3)
			i += 1
			# print(wmsR)
		path = os.getcwd() + "\..\\"
		os.chdir(path)

print("Hello")
site1 = site1.to_numpy()
# print(site1)
print("Hello")

p_rows, p_cols = site1.shape
sum = 0.0
for i in range(p_rows):
	sum += site1[i][3]

print(sum)