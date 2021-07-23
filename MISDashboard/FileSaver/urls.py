from django.urls import path, include
from . import views

urlpatterns = [
	path('4-0-4/', views.error_page, name='error_page'),
	path('sites-liveupdates/', views.dailyupdates, name='dailyupdates'),
	path('getting-started/', views.startdoc, name='startdoc'),
	path('analysis-window/', views.analysis, name='analysis'),
	path('exception-report/', views.report, name='report'),
]