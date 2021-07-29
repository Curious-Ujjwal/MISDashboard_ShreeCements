##Feature to be added:

-> Sub-feature 1 : 

 - Auto-opening of emails -- DONE
 - Read the emails with the attachments -- DONE
 - Download those attachments -- DONE
 - Store them in a folder -- DONE

-> Auto opening of emails through smtplib  -- DONE
-> Download the .csv/.xlsx files from the mails -- DONE
-> Save the files in the local folders -- DONE
-> Save these files in a separate directory -- DONE
    ..Directory structure
    /SiteSheets/Date/Site1Data
                    /Site2Data
                    /Site3Data
                    /Site4Data
                Date in default format
-> Store the files according to the data-timestamp -- DONE
-> Batch file for automating downloads -- DONE
   (Make action on Task Scheduler to execute this batch file)
-> Make models for final CSV datesheet -- DONE
-> Collecting the CSV data of four sheets in different variables -- DONE
-> Declutter all the data from those variables, just keeping only data-containing cells -- DONE
-> Function for calculating the final values for the combined sheet from various dataframes -- DONE
-> one redirect url to call a request-based authentication and authorisation to save the final sheet variables
-> Customise Sheet model to add the operator entries, like as mentioned in the models.py file -- DONE
-> Make the dashboard design FRONTEND, and send it to the mentors for review -- DONE
    -> Basic layout and common features -- DONE
    -> Login function, Date filter, Representation through Charts, and then the table-view, save the table feature -- DONE
    -> Guide to use the dashboard, and admin panel
-> Connect the FRONTEND and BACKEND -- DONE
-> Customise the django-admin panel according to the Company's Website color scheme. -- DONE
-> and then review the code for debug purposes
-> Prepare the Report (1st Draft) -- DONE
-> Prepare the PPT (1st Draft)

##Features to be tested on the server while deploying:
-> Make Task Scheduler to execute the batch file(filestorehelp.bat) every day
-> Make Task Scheduler to execute the batch file for cleanup.py
-> Organise the url for later tasks, LOL