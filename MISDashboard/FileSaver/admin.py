from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from .models import *
# from .forms import *


# Register your models here.

class Panipat_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date',DateRangeFilter), )
	date_hierarchy = 'date'
	ordering = ('-date',)
	# form = EntryForm
	# class Media:
	# 	css = {
 #            'all': ('fancy.css',)
 #        }

admin.site.register(Panipat_Sheet, Panipat_SheetAdmin)

class Castamet_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	# form = EntryForm

admin.site.register(Castamet_Sheet, Castamet_SheetAdmin)

class Jharkhand_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	# form = EntryForm

admin.site.register(Jharkhand_Sheet, Jharkhand_SheetAdmin)

class Roorkee_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	# form = EntryForm

admin.site.register(Roorkee_Sheet, Roorkee_SheetAdmin)

class Beawar_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	# form = EntryForm

admin.site.register(Beawar_Sheet, Beawar_SheetAdmin)

@admin.register(Operator_Entry)
class Operator_EntryAdmin(admin.ModelAdmin):
	pass