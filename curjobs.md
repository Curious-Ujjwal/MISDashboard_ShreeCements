##Feature to be added:

-> Sub-feature 1 : 

 - Auto-opening of emails
 - Read the emails with the attachments
 - Download those attachments 
 - Store them in a folder

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
-> Collecting the CSV data of four sheets in different variables -- 
-> Declutter all the data from those variables, just keeping only data-containing cells --
-> Then, the function for preparing the combined data sheet in the required format --
-> Function for storing that in Django database. [includes authentication, automation of Session cookie] --
-> Function to pass the data from the final-sheet(s) onto the webpage --