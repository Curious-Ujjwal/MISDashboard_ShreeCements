from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from decimal import Decimal
from .defineconstants import *
from datetime import date
from .models import *
# from .forms import *

today = date.today().strftime('%d-%m-%Y')
day = int(today[:2])
month = int(today[3:5])
year = int(today[6:])

# Register your models here.

class Panipat_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date',DateRangeFilter), )
	date_hierarchy = 'date'
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
		('Target & Actual Irradiance', {
				'fields': (
				 	('daily_target_irradiance', 'monthly_target_irradiance', 'yearly_target_irradiance'),
	 				('daily_actual_irradiance', 'monthly_actual_irradiance', 'yearly_actual_irradiance'),
				)
			}),
		('Target & Actual Performance Ratios', {
				'fields': (
					('daily_target_performance_ratio', 'monthly_target_performance_ratio', 'yearly_target_performance_ratio'),
					('daily_actual_performance_ratio', 'monthly_actual_performance_ratio', 'yearly_actual_performance_ratio'),
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
	# read_only_fields = ('monthly_actual_irradiance', )


	#Function for calculations based on user input
	def save_model(self, request, obj, form, change):
		month_irradiance_till_date = 0.0
		monthly_irradiance_loss_till_date = 0.0
		monthly_deemedloss_till_date = 0.0
		monthly_gridloss_till_date = 0.0
		monthly_bdloss_till_date = 0.0
		monthly_dustloss_till_date = 0.0
		yearly_target_gen_till_date = 0.0
		yearly_deemedloss_till_date = 0.0
		yearly_gridloss_till_date = 0.0
		yearly_bdloss_till_date = 0.0
		yearly_dustloss_till_date = 0.0
		annual_actual_irradiance_till_date = 0.0
		irradiation_sum = 0.00 	#This contains the sum fo target irradiation based on kWh for over a month
		yearly_irradianceloss_till_date = 0.0
		yearly_tg_till_date = 0.0

		try:
			last_record = Panipat_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
				month_irradiance_till_date = 0.0
				month_irradiance_till_date = 0.0
				monthly_deemedloss_till_date = 0.00
				monthly_gridloss_till_date = 0.00
				monthly_bdloss_till_date = 0.00
				monthly_dustloss_till_date = 0.00


			yearly_target_gen_till_date = last_record.yearly_target_generation
			yearly_deemedloss_till_date = last_record.yearly_deemed_loss
			yearly_gridloss_till_date = last_record.yearly_grid_loss
			yearly_bdloss_till_date = last_record.yearly_bd_loss
			yearly_dustloss_till_date = last_record.yearly_dust_loss
			annual_actual_irradiance_till_date = last_record.yearly_actual_irradiance
			yearly_irradianceloss_till_date = last_record.yearly_irradiance_loss
			yearly_tg_till_date = last_record.yearly_target_generation
			irradiation_sum = (float(yearly_tg_till_date)/(panipat_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(panipat_constant*24))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(panipat_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(panipat_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(panipat_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(panipat_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant*(obj.days_elapsed)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(panipat_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(panipat_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(panipat_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(panipat_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_plf
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(panipat_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(panipat_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(panipat_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_misc_loss = yearly_generation_loss - obj.yearly_irradiance_loss - obj.yearly_deemed_loss_plf - obj.yearly_grid_loss_plf - obj.yearly_bd_loss_plf - obj.yearly_dust_loss_plf


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
		month_irradiance_till_date = 0.0
		monthly_irradiance_loss_till_date = 0.0
		monthly_deemedloss_till_date = 0.0
		monthly_gridloss_till_date = 0.0
		monthly_bdloss_till_date = 0.0
		monthly_dustloss_till_date = 0.0
		yearly_target_gen_till_date = 0.0
		yearly_deemedloss_till_date = 0.0
		yearly_gridloss_till_date = 0.0
		yearly_bdloss_till_date = 0.0
		yearly_dustloss_till_date = 0.0
		annual_actual_irradiance_till_date = 0.0
		irradiation_sum = 0.00 	#This contains the sum fo target irradiation based on kWh for over a month
		yearly_irradianceloss_till_date = 0.0
		yearly_tg_till_date = 0.0

		try:
			last_record = Panipat_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
				month_irradiance_till_date = 0.0
				month_irradiance_till_date = 0.0
				monthly_deemedloss_till_date = 0.00
				monthly_gridloss_till_date = 0.00
				monthly_bdloss_till_date = 0.00
				monthly_dustloss_till_date = 0.00


			yearly_target_gen_till_date = last_record.yearly_target_generation
			yearly_deemedloss_till_date = last_record.yearly_deemed_loss
			yearly_gridloss_till_date = last_record.yearly_grid_loss
			yearly_bdloss_till_date = last_record.yearly_bd_loss
			yearly_dustloss_till_date = last_record.yearly_dust_loss
			annual_actual_irradiance_till_date = last_record.yearly_actual_irradiance
			yearly_irradianceloss_till_date = last_record.yearly_irradiance_loss
			yearly_tg_till_date = last_record.yearly_target_generation
			irradiation_sum = (float(yearly_tg_till_date)/(panipat_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(panipat_constant*24))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(panipat_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(panipat_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(panipat_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(panipat_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant*(obj.days_elapsed)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(panipat_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(panipat_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(panipat_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(panipat_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_plf
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(panipat_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(panipat_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(panipat_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_misc_loss = yearly_generation_loss - obj.yearly_irradiance_loss - obj.yearly_deemed_loss_plf - obj.yearly_grid_loss_plf - obj.yearly_bd_loss_plf - obj.yearly_dust_loss_plf


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
		month_irradiance_till_date = 0.0
		monthly_irradiance_loss_till_date = 0.0
		monthly_deemedloss_till_date = 0.0
		monthly_gridloss_till_date = 0.0
		monthly_bdloss_till_date = 0.0
		monthly_dustloss_till_date = 0.0
		yearly_target_gen_till_date = 0.0
		yearly_deemedloss_till_date = 0.0
		yearly_gridloss_till_date = 0.0
		yearly_bdloss_till_date = 0.0
		yearly_dustloss_till_date = 0.0
		annual_actual_irradiance_till_date = 0.0
		irradiation_sum = 0.00 	#This contains the sum fo target irradiation based on kWh for over a month
		yearly_irradianceloss_till_date = 0.0
		yearly_tg_till_date = 0.0

		try:
			last_record = Panipat_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
				month_irradiance_till_date = 0.0
				month_irradiance_till_date = 0.0
				monthly_deemedloss_till_date = 0.00
				monthly_gridloss_till_date = 0.00
				monthly_bdloss_till_date = 0.00
				monthly_dustloss_till_date = 0.00


			yearly_target_gen_till_date = last_record.yearly_target_generation
			yearly_deemedloss_till_date = last_record.yearly_deemed_loss
			yearly_gridloss_till_date = last_record.yearly_grid_loss
			yearly_bdloss_till_date = last_record.yearly_bd_loss
			yearly_dustloss_till_date = last_record.yearly_dust_loss
			annual_actual_irradiance_till_date = last_record.yearly_actual_irradiance
			yearly_irradianceloss_till_date = last_record.yearly_irradiance_loss
			yearly_tg_till_date = last_record.yearly_target_generation
			irradiation_sum = (float(yearly_tg_till_date)/(panipat_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(panipat_constant*24))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(panipat_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(panipat_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(panipat_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(panipat_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant*(obj.days_elapsed)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(panipat_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(panipat_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(panipat_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(panipat_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_plf
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(panipat_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(panipat_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(panipat_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_misc_loss = yearly_generation_loss - obj.yearly_irradiance_loss - obj.yearly_deemed_loss_plf - obj.yearly_grid_loss_plf - obj.yearly_bd_loss_plf - obj.yearly_dust_loss_plf


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
		month_irradiance_till_date = 0.0
		monthly_irradiance_loss_till_date = 0.0
		monthly_deemedloss_till_date = 0.0
		monthly_gridloss_till_date = 0.0
		monthly_bdloss_till_date = 0.0
		monthly_dustloss_till_date = 0.0
		yearly_target_gen_till_date = 0.0
		yearly_deemedloss_till_date = 0.0
		yearly_gridloss_till_date = 0.0
		yearly_bdloss_till_date = 0.0
		yearly_dustloss_till_date = 0.0
		annual_actual_irradiance_till_date = 0.0
		irradiation_sum = 0.00 	#This contains the sum fo target irradiation based on kWh for over a month
		yearly_irradianceloss_till_date = 0.0
		yearly_tg_till_date = 0.0

		try:
			last_record = Panipat_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
				month_irradiance_till_date = 0.0
				month_irradiance_till_date = 0.0
				monthly_deemedloss_till_date = 0.00
				monthly_gridloss_till_date = 0.00
				monthly_bdloss_till_date = 0.00
				monthly_dustloss_till_date = 0.00


			yearly_target_gen_till_date = last_record.yearly_target_generation
			yearly_deemedloss_till_date = last_record.yearly_deemed_loss
			yearly_gridloss_till_date = last_record.yearly_grid_loss
			yearly_bdloss_till_date = last_record.yearly_bd_loss
			yearly_dustloss_till_date = last_record.yearly_dust_loss
			annual_actual_irradiance_till_date = last_record.yearly_actual_irradiance
			yearly_irradianceloss_till_date = last_record.yearly_irradiance_loss
			yearly_tg_till_date = last_record.yearly_target_generation
			irradiation_sum = (float(yearly_tg_till_date)/(panipat_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(panipat_constant*24))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(panipat_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(panipat_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(panipat_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(panipat_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant*(obj.days_elapsed)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(panipat_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(panipat_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(panipat_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(panipat_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_plf
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(panipat_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(panipat_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(panipat_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_misc_loss = yearly_generation_loss - obj.yearly_irradiance_loss - obj.yearly_deemed_loss_plf - obj.yearly_grid_loss_plf - obj.yearly_bd_loss_plf - obj.yearly_dust_loss_plf


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
		month_irradiance_till_date = 0.0
		monthly_irradiance_loss_till_date = 0.0
		monthly_deemedloss_till_date = 0.0
		monthly_gridloss_till_date = 0.0
		monthly_bdloss_till_date = 0.0
		monthly_dustloss_till_date = 0.0
		yearly_target_gen_till_date = 0.0
		yearly_deemedloss_till_date = 0.0
		yearly_gridloss_till_date = 0.0
		yearly_bdloss_till_date = 0.0
		yearly_dustloss_till_date = 0.0
		annual_actual_irradiance_till_date = 0.0
		irradiation_sum = 0.00 	#This contains the sum fo target irradiation based on kWh for over a month
		yearly_irradianceloss_till_date = 0.0
		yearly_tg_till_date = 0.0

		try:
			last_record = Panipat_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
				month_irradiance_till_date = 0.0
				month_irradiance_till_date = 0.0
				monthly_deemedloss_till_date = 0.00
				monthly_gridloss_till_date = 0.00
				monthly_bdloss_till_date = 0.00
				monthly_dustloss_till_date = 0.00


			yearly_target_gen_till_date = last_record.yearly_target_generation
			yearly_deemedloss_till_date = last_record.yearly_deemed_loss
			yearly_gridloss_till_date = last_record.yearly_grid_loss
			yearly_bdloss_till_date = last_record.yearly_bd_loss
			yearly_dustloss_till_date = last_record.yearly_dust_loss
			annual_actual_irradiance_till_date = last_record.yearly_actual_irradiance
			yearly_irradianceloss_till_date = last_record.yearly_irradiance_loss
			yearly_tg_till_date = last_record.yearly_target_generation
			irradiation_sum = (float(yearly_tg_till_date)/(panipat_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(panipat_constant*24))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(panipat_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(panipat_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(panipat_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(panipat_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant*(obj.days_elapsed)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(panipat_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(panipat_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(panipat_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(panipat_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_plf
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(panipat_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(panipat_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(panipat_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(panipat_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_misc_loss = yearly_generation_loss - obj.yearly_irradiance_loss - obj.yearly_deemed_loss_plf - obj.yearly_grid_loss_plf - obj.yearly_bd_loss_plf - obj.yearly_dust_loss_plf


		super().save_model(request, obj, form, change)




	# form = EntryForm

admin.site.register(Beawar_Sheet, Beawar_SheetAdmin)

@admin.register(Operator_Entry)
class Operator_EntryAdmin(admin.ModelAdmin):
	pass