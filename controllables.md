This file contains all the necessary requirements for running this MIS:
1. Email settings of Shree Cement has to be set to point to its IMAP.
2. FIle-download script has to be scheduled for every day at a particular timestamp.
3. Cleanup script has to be scheduled at month's end.
4. In django-admin, the entries about the sites have to be deleted manually, as per the values.
5. All the site sheets and WMS reports should be in the .xslx format, otherwise error will be thrown.
6. All the sheets must have permission to edit, format or delete the entry, otherwsie the software will not be able to read the files.