from django.contrib import admin
from .models import SiteSheet
from rangefilter.filters import DateRangeFilter

# Register your models here.

class SiteSheetAdmin(admin.ModelAdmin):
	list_filter = (('date',DateRangeFilter), )
	list_display=('date', 'site1', 'site2', 'site3', 'site4')
	date_hierarchy = 'date'
	class Media:
		css = {
            'all': ('fancy.css',)
        }

admin.site.register(SiteSheet, SiteSheetAdmin)