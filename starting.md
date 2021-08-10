Starting instructions for this project:
1. Pre-requisites: [Bootstrap+ChartJS (FrontEnd)] & [Django (BackEnd)]
2. All the controllable variables are mentioned in controllables.md explicitly[need to be carefully followed].
3. If in case of adding new sites, extend more models in models.py file.
4. Email download script and cleanup script have to be scheduled on local computer on which the software is hosted.
5. Email download script is included in views.py file, .bat file for the same is stored in MISDashboard folder.
6. Cleanup script is cleanup.py, included in MISDashboard folder.
7. Manual cleaning of the database is mandatory.
8. The different constants for each site like seasonal_tilt and max_power are defined in defineconstants.py file.
9. Currently, at any day, the downloaded files are read and stored in separate variables as can be found in utilityfunction.py file. The variables are created daily as the new sheets are downloaded.
10. Email subjects need to be properly configured.
a) Email containing WMS report should have 'wms' and sitename in subject.
b) Email containing SiteSheet need to only have sitename in subject.