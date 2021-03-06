from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.userlogin, name='userlogin'),
	path('4-0-4/', views.error_page, name='error_page'),
	path('sites-liveupdates/', views.dailyupdates, name='dailyupdates'),
	path('getting-started/', views.startdoc, name='startdoc'),
	path('analysis-window/', views.analysis, name='analysis'),
	path('exception-report/', views.report, name='report'),
	path('analysis-window-among-sites', views.siteanalysis, name='siteanalysis'),
	path('analysis-in-a-site', views.invertoranalysis, name='invertoranalysis'),
	path('getdetails/', views.getdetails, name='getdetails'),	#AJAX URL
]