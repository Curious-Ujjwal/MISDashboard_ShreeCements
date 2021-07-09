#This script is mde to execute monthly to remove all the downloaded scripts from the DJANGO mysql database.
import os

path = os.getcwd()+"\..\..\SiteSheets"
os.chdir(path)

print(path)

listing = [str(l) for l in os.listdir(path='.')]
#all folders will be for different dates

path_to_folder = None

for folder in listing:
	#for every date folder
	if folder is not None:
		path = os.getcwd() + '\\' + folder
		os.chdir(path)
		
		folderlist = [str[fs] for fs in os.listdir(path='.')]
		#list of all the folders of a particular date including Site Reports and WMS reports.

		for eachfolder in folderlist:
			if eachfolder is not None: 
			#for every folder whether a WMS report or Site Report
				
				path = os.getcwd() + "\\" + eachfolder
				os.chdir(path)
				filelist = [str(file) for file in os.listdir(path='.')]
				#there will be only one file per folder here.

				file = filelist[0]
				print(file)
				os.remove(file)
				#remove the file

				path_to_folder = path
				path = os.getcwd()+"\.."

				#remove the subfolder where file was stored
				os.chdir(path)
				os.rmdir(path_to_folder)
		
		path_to_folder = path
		path = os.getcwd()+"\.."
		os.chdir(path)
		os.rmdir(path_to_folder) 