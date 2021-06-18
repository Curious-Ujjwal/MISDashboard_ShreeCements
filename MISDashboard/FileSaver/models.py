from django.db import models
from datetime import datetime
import datetime

# Create your models here.
class SiteSheet(models.Model):
	site1 = models.FileField(upload_to='')
	email1 = models.EmailField(max_length=30)
	site2 = models.FileField(upload_to='')
	email2 = models.EmailField(max_length=30)
	site3 = models.FileField(upload_to='')
	email3 = models.EmailField(max_length=30)
	site4 = models.FileField(upload_to='')
	email4 = models.EmailField(max_length=30)
	date = models.DateField(default=datetime.date.today)