from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from .defineconstants import *
from .models import *
# from .forms import *


# Register your models here.

class Panipat_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date',DateRangeFilter), )
	date_hierarchy = 'date'
	ordering = ('-date',)
	actions_on_top = True 	#so that the action changelist bar displays on the top
	actions_on_bottom = True 	#so that the action changelist bar displays on the bottom
	empty_value_display = '-empty-'
	list_max_show_all = 366
	# read_only_fields = ('', )
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh)', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh)', {
				'fields': (
					('daily_target_generation', 'monthly_target_generation', 'yearly_target_generation'),
					('daily_actual_generation', 'monthly_actual_generation', 'yearly_actual_generation'),
				)
			}),
		('Target & Actual PLF (in %)', {
				'fields': (
					('daily_target_plf', 'monthly_target_plf', 'yearly_target_plf',),
					('daily_actual_plf', 'monthly_actual_plf', 'yearly_actual_plf'),
				)
			}),
		('Target & Actual Performance Ratios', {
				'fields': (
					('daily_target_performance_ratio', 'monthly_target_performance_ratio', 'yearly_target_performance_ratio'),
					('daily_actual_performance_ratio', 'monthly_actual_performance_ratio', 'yearly_actual_performance_ratio'),
				)
			}),
		('Target & Actual Irradiance', {
				'fields': (
				 	('daily_target_irradiance', 'monthly_target_irradiance', 'yearly_target_irradiance'),
	 				('daily_actual_irradiance', 'monthly_actual_irradiance', 'yearly_actual_irradiance'),
				)
			}),
		('Loss due to Irradiance', {
				'fields': (('daily_irradiance_loss', 'monthly_irradiance_loss', 'yearly_irradiance_loss'),)
			}),
		('Deemed Loss', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to grid outage', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
	)

	#Function for calculations based on user input
	def save_model(self, request, obj, form, change):
		if form.has_changed():
			#Calculation of daily parameters
			obj.daily_target_plf = ((float(obj.daily_target_generation))/(panipat_constant*24))*100
			obj.daily_actual_performance_ratio = ((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100
			obj.daily_irradiance_loss = obj.daily_target_plf - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = ((float(obj.daily_deemed_loss))/(panipat_constant*24))*100
			obj.daily_grid_loss_plf = ((float(obj.daily_grid_loss))/(panipat_constant*24))*100
			obj.daily_bd_loss_plf = ((float(obj.daily_bd_loss))/(panipat_constant*24))*100
			obj.daily_dust_loss_plf = ((float(obj.daily_dust_loss))/(panipat_constant*24))*100
			generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			
		super().save_model(request, obj, form, change)
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
	actions_on_top = True 	#so that the action changelist bar displays on the top
	actions_on_bottom = True 	#so that the action changelist bar displays on the bottom
	empty_value_display = '-empty-'
	list_max_show_all = 366
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh)', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh)', {
				'fields': (
					('daily_target_generation', 'monthly_target_generation', 'yearly_target_generation'),
					('daily_actual_generation', 'monthly_actual_generation', 'yearly_actual_generation'),
				)
			}),
		('Target & Actual PLF (in %)', {
				'fields': (
					('daily_target_plf', 'monthly_target_plf', 'yearly_target_plf',),
					('daily_actual_plf', 'monthly_actual_plf', 'yearly_actual_plf'),
				)
			}),
		('Target & Actual Performance Ratios', {
				'fields': (
					('daily_target_performance_ratio', 'monthly_target_performance_ratio', 'yearly_target_performance_ratio'),
					('daily_actual_performance_ratio', 'monthly_actual_performance_ratio', 'yearly_actual_performance_ratio'),
				)
			}),
		('Target & Actual Irradiance', {
				'fields': (
				 	('daily_target_irradiance', 'monthly_target_irradiance', 'yearly_target_irradiance'),
	 				('daily_actual_irradiance', 'monthly_actual_irradiance', 'yearly_actual_irradiance'),
				)
			}),
		('Deemed Loss', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to Irradiance', {
				'fields': (('daily_irradiance_loss', 'monthly_irradiance_loss', 'yearly_irradiance_loss'),)
			}),
		('Loss due to grid outage', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
	)

	def save_model(self, request, obj, form, change):
		if form.has_changed():
			#Calculation of daily parameters
			obj.daily_target_plf = ((float(obj.daily_target_generation))/(panipat_constant*24))*100
			obj.daily_actual_performance_ratio = ((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100
			obj.daily_irradiance_loss = obj.daily_target_plf - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = ((float(obj.daily_deemed_loss))/(panipat_constant*24))*100
			obj.daily_grid_loss_plf = ((float(obj.daily_grid_loss))/(panipat_constant*24))*100
			obj.daily_bd_loss_plf = ((float(obj.daily_bd_loss))/(panipat_constant*24))*100
			obj.daily_dust_loss_plf = ((float(obj.daily_dust_loss))/(panipat_constant*24))*100
			generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf
			


		super().save_model(request, obj, form, change)

	# form = EntryForm

admin.site.register(Castamet_Sheet, Castamet_SheetAdmin)

class Jharkhand_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	actions_on_top = True 	#so that the action changelist bar displays on the top
	actions_on_bottom = True 	#so that the action changelist bar displays on the bottom
	empty_value_display = '-empty-'
	list_max_show_all = 366
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh)', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh)', {
				'fields': (
					('daily_target_generation', 'monthly_target_generation', 'yearly_target_generation'),
					('daily_actual_generation', 'monthly_actual_generation', 'yearly_actual_generation'),
				)
			}),
		('Target & Actual PLF (in %)', {
				'fields': (
					('daily_target_plf', 'monthly_target_plf', 'yearly_target_plf',),
					('daily_actual_plf', 'monthly_actual_plf', 'yearly_actual_plf'),
				)
			}),
		('Target & Actual Performance Ratios', {
				'fields': (
					('daily_target_performance_ratio', 'monthly_target_performance_ratio', 'yearly_target_performance_ratio'),
					('daily_actual_performance_ratio', 'monthly_actual_performance_ratio', 'yearly_actual_performance_ratio'),
				)
			}),
		('Target & Actual Irradiance', {
				'fields': (
				 	('daily_target_irradiance', 'monthly_target_irradiance', 'yearly_target_irradiance'),
	 				('daily_actual_irradiance', 'monthly_actual_irradiance', 'yearly_actual_irradiance'),
				)
			}),
		('Deemed Loss', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to Irradiance', {
				'fields': (('daily_irradiance_loss', 'monthly_irradiance_loss', 'yearly_irradiance_loss'),)
			}),
		('Loss due to grid outage', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
	)

	def save_model(self, request, obj, form, change):
		if form.has_changed():
			#Calculation of daily parameters
			obj.daily_target_plf = ((float(obj.daily_target_generation))/(panipat_constant*24))*100
			obj.daily_actual_performance_ratio = ((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100
			obj.daily_irradiance_loss = obj.daily_target_plf - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = ((float(obj.daily_deemed_loss))/(panipat_constant*24))*100
			obj.daily_grid_loss_plf = ((float(obj.daily_grid_loss))/(panipat_constant*24))*100
			obj.daily_bd_loss_plf = ((float(obj.daily_bd_loss))/(panipat_constant*24))*100
			obj.daily_dust_loss_plf = ((float(obj.daily_dust_loss))/(panipat_constant*24))*100
			generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


		super().save_model(request, obj, form, change)


	# form = EntryForm

admin.site.register(Jharkhand_Sheet, Jharkhand_SheetAdmin)

class Roorkee_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	actions_on_top = True 	#so that the action changelist bar displays on the top
	actions_on_bottom = True 	#so that the action changelist bar displays on the bottom
	empty_value_display = '-empty-'
	list_max_show_all = 366
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh)', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh)', {
				'fields': (
					('daily_target_generation', 'monthly_target_generation', 'yearly_target_generation'),
					('daily_actual_generation', 'monthly_actual_generation', 'yearly_actual_generation'),
				)
			}),
		('Target & Actual PLF (in %)', {
				'fields': (
					('daily_target_plf', 'monthly_target_plf', 'yearly_target_plf',),
					('daily_actual_plf', 'monthly_actual_plf', 'yearly_actual_plf'),
				)
			}),
		('Target & Actual Performance Ratios', {
				'fields': (
					('daily_target_performance_ratio', 'monthly_target_performance_ratio', 'yearly_target_performance_ratio'),
					('daily_actual_performance_ratio', 'monthly_actual_performance_ratio', 'yearly_actual_performance_ratio'),
				)
			}),
		('Target & Actual Irradiance', {
				'fields': (
				 	('daily_target_irradiance', 'monthly_target_irradiance', 'yearly_target_irradiance'),
	 				('daily_actual_irradiance', 'monthly_actual_irradiance', 'yearly_actual_irradiance'),
				)
			}),
		('Deemed Loss', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to Irradiance', {
				'fields': (('daily_irradiance_loss', 'monthly_irradiance_loss', 'yearly_irradiance_loss'),)
			}),
		('Loss due to grid outage', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
	)

	def save_model(self, request, obj, form, change):
		if form.has_changed():
			#Calculation of daily parameters
			obj.daily_target_plf = ((float(obj.daily_target_generation))/(panipat_constant*24))*100
			obj.daily_actual_performance_ratio = ((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100
			obj.daily_irradiance_loss = obj.daily_target_plf - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = ((float(obj.daily_deemed_loss))/(panipat_constant*24))*100
			obj.daily_grid_loss_plf = ((float(obj.daily_grid_loss))/(panipat_constant*24))*100
			obj.daily_bd_loss_plf = ((float(obj.daily_bd_loss))/(panipat_constant*24))*100
			obj.daily_dust_loss_plf = ((float(obj.daily_dust_loss))/(panipat_constant*24))*100
			generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


		super().save_model(request, obj, form, change)



	# form = EntryForm

admin.site.register(Roorkee_Sheet, Roorkee_SheetAdmin)

class Beawar_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date', DateRangeFilter), )
	date_hierarchy='date'
	ordering = ('-date',)
	actions_on_top = True 	#so that the action changelist bar displays on the top
	actions_on_bottom = True 	#so that the action changelist bar displays on the bottom
	empty_value_display = '-empty-' 
	list_max_show_all = 366
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh)', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh)', {
				'fields': (
					('daily_target_generation', 'monthly_target_generation', 'yearly_target_generation'),
					('daily_actual_generation', 'monthly_actual_generation', 'yearly_actual_generation'),
				)
			}),
		('Target & Actual PLF (in %)', {
				'fields': (
					('daily_target_plf', 'monthly_target_plf', 'yearly_target_plf',),
					('daily_actual_plf', 'monthly_actual_plf', 'yearly_actual_plf'),
				)
			}),
		('Target & Actual Performance Ratios', {
				'fields': (
					('daily_target_performance_ratio', 'monthly_target_performance_ratio', 'yearly_target_performance_ratio'),
					('daily_actual_performance_ratio', 'monthly_actual_performance_ratio', 'yearly_actual_performance_ratio'),
				)
			}),
		('Target & Actual Irradiance', {
				'fields': (
				 	('daily_target_irradiance', 'monthly_target_irradiance', 'yearly_target_irradiance'),
	 				('daily_actual_irradiance', 'monthly_actual_irradiance', 'yearly_actual_irradiance'),
				)
			}),
		('Deemed Loss', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to Irradiance', {
				'fields': (('daily_irradiance_loss', 'monthly_irradiance_loss', 'yearly_irradiance_loss'),)
			}),
		('Loss due to grid outage', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
	)

	def save_model(self, request, obj, form, change):
		if form.has_changed():
			#Calculation of daily parameters
			obj.daily_target_plf = ((float(obj.daily_target_generation))/(panipat_constant*24))*100
			obj.daily_actual_performance_ratio = ((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100
			obj.daily_irradiance_loss = obj.daily_target_plf - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = ((float(obj.daily_deemed_loss))/(panipat_constant*24))*100
			obj.daily_grid_loss_plf = ((float(obj.daily_grid_loss))/(panipat_constant*24))*100
			obj.daily_bd_loss_plf = ((float(obj.daily_bd_loss))/(panipat_constant*24))*100
			obj.daily_dust_loss_plf = ((float(obj.daily_dust_loss))/(panipat_constant*24))*100
			generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf
			

			
		super().save_model(request, obj, form, change)



	# form = EntryForm

admin.site.register(Beawar_Sheet, Beawar_SheetAdmin)

@admin.register(Operator_Entry)
class Operator_EntryAdmin(admin.ModelAdmin):
	pass