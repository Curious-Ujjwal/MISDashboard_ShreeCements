#This script is mde to execute monthly to remove all the downloaded scripts from the DJANGO mysql database.
import os

path = os.getcwd()+"\..\..\SiteSheets"
os.chdir(path)

print(path)

listing = [str(l) for l in os.listdir(path='.')]
#all folders will be for different dates

path_to_folder = None

for folder in listing:#for every date folder
	if folder is not None:
		path = os.getcwd() + '\\' + folder
		os.chdir(path)
		
		folderlist = [str[fs] for fs in os.listdir(path='.')]
		#list of all the 4 folders of a particular date

		for eachfolder in folderlist:
			if eachfolder is not None:
				path = os.getcwd() + "\\" + eachfolder
				os.chdir(path)
				filelist = [str(file) for file in os.listdir(path='.')]
				file = filelist[0]
				print(file)
				os.remove(file)
				path_to_folder = path
				path = os.getcwd()+"\.."
				os.chdir(path)
				os.rmdir(path_to_folder)
		
		path_to_folder = path
		path = os.getcwd()+"\.."
		os.chdir(path)
		os.rmdir(path_to_folder) 