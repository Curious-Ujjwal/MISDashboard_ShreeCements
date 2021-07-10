from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from .models import *
from .forms import *


# Register your models here.

class Panipat_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date',DateRangeFilter), )
	date_hierarchy = 'date'
	form = EntryForm
	# class Media:
	# 	css = {
 #            'all': ('fancy.css',)
 #        }

admin.site.register(Panipat_Sheet, Panipat_SheetAdmin)

@admin.register(Operator_Entry)
class Operator_EntryAdmin(admin.ModelAdmin):
	pass