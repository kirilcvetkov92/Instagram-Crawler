# Instagram-Crawler
This project we cover several segments of data collection on Instagram and their presentation 1. Python scrip solution that captures/craws data from Instagram. 2. Enter the collected instagram profile information in the database. 3. View and filter the data on a simple WEB site in Django Framemwork. 4. Practical application

## INSTALLATION REQUIREMENTS
 
* Install Python 3.6.0
* Install the Pip Package, type in the command line:
  
  ***python get-pip.py***
* Install Pip requests (This will install Django and Selenium frames)
  
  ***cd * PATH * / Project*** 
  
  ***pip install -r requirements.txt***
* Install Firefox Client (you can download the famous Mozilla Firefox browser)
* Completed



## SETTING UP THE WEB SYSTEM
* If you want to use the web system, then you need to deploy the entire Django system in the database. We do this with the following code:

  ***cd * PATH * / Project / web. / manage.py makemigrations***

This will perform the migrations from the model. /manage.py migrate Convert migrations from a model to a base

* Default user/admin access : 
 
  * user : admin
  * password : admin
  
* To create a Super Administrator who has all the privileges, type:

  ***./manage.py createsuperuser***

Enter the fields that are required.

* To turn on the server, run the following command and activate the Django Web application at port 8000

  ***./manage.py runserver 8000***
