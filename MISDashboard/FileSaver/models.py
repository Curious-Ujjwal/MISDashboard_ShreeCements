from django.db import models
from datetime import datetime
import datetime

# Create your models here.
class SiteSheet(models.Model):
	site1 = models.FileField(upload_to='')
	site2 = models.FileField(upload_to='')
	site3 = models.FileField(upload_to='')
	site4 = models.FileField(upload_to='')
	date = models.DateField(default=datetime.date.today)