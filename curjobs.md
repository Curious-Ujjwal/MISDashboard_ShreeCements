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
-> Make the dashboard design FRONTEND, and send it to the mentors for review
    -> Basic layout and common features -- DONE
    -> Login function, Date filter, Representation through Charts, and then the table-view, save the table feature -- DONE
    -> Guide to use the dashboard, and admin panel
-> Connect the FRONTEND and BACKEND
-> Customise the django-admin panel according to the Company's Website color scheme. -- DONE
-> and then review the code for debug purposes
-> Prepare the Report (1st Draft)
-> Prepare the PPT (1st Draft)

##Features to be tested on the server while deploying:
-> Make Task Scheduler to execute the batch file(filestorehelp.bat) every day
-> Make Task Scheduler to execute the batch file for cleanup.py
-> Organise the url for later tasks, LOL




##DOUBTS
1. Solar Base Report ke doubts
    Panipat location mei 2 sheets ka locha -- SOLVED
    Irradiation ka formula -- SOLVEDD
    target_plf_based_on_actual_irradiation formula -- SOLVED
    Are all parameters calcualted for all locations? Some losses are not filled in the sheets -- SOLVED
    Deemed loss ka formula/ and is it only calculated for Panipat and Beawar? -- SOLVED
    Grid Outage loss ka formula -- SOLVED
    BD loss ka formula -- SOLVED
    Dust loss ka formula -- SOLVED

2. In Panipat irradiance, weighted mean is calculated, where to get those values. Chekced values but not coming same as sheet -- SOLVED
3. Will BD loss always be 0? Or for some sites like Beawar & Panipat, we have to look from the Solar Base Report -- SOLVED
4. What is the meaning of $AM$3 in excel?
5. For some yearly calculation Bckup Sheet is required, will ie be provided, or can you tell me where I can find the value -- SOLVED
6. from where to take the data for the cells, where Panipat is written in formula bar, like = Panipat!M43 -- SOLVED