from FileSaver.models import *

last_record = None
count_till_date = 0

try:
	last_record = Panipat_Sheet.objects.latest('date')
	count_till_date = Panipat_Sheet.objects.all().count()
except:
	last_record = None
	count_till_date = 0

print(last_record)
print(count_till_date)