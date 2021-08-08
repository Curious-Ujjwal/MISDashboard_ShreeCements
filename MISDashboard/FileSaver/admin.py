from rangefilter.filters import DateRangeFilter
from django.contrib import admin
from decimal import Decimal
from .defineconstants import *
from datetime import date
from .models import *
import datetime

#Calcualting today's date, month and year for calculation purposes
prev_datetime = datetime.datetime.today() - datetime.timedelta(days=1)
prev_day = prev_datetime.strftime('%d-%m-%Y')
#As on any day, we are always getting the data of one day before
today = prev_day

day = int(today[:2])
month = int(today[3:5])
year = int(today[6:])

# Register your models here.


"""
	For all the classes Panipat_SheetAdmin, Castamet_SheetAdmin, Jharkhand_SheetAdmin, Roorkee_SheetAdmin, Beawar_SheetAdmin
	Read the following:
	-> The records are filtered by date through DateRangeFilter
	-> All the records are ordered in django-admin by the reverse order of date using ordering
	-> Actions for deleting, saving are displayed on top and bottom using actions_on_top, actions_on_bottom
	-> If the attribute is empty, it will be displayed -empty- , if it is not necesary to be filled.
	-> Max records to be shown are - 366. using list_max_show_all
	-> Then fieldsets are defined for managing the display of various features. using fieldsets

	-> Then anytime, a model value is changed, some particulars which maybe dependent on these variables are calculated based on those variables.
	-> save_model: function that helps to achieve the above
	-> first some temporary variables are defined for in-between calculation

	-> Calculations occur as follows: 
	-> if any record exists in a sheet, that is taken as last_record
	-> Then check if the today's date's month is same as last_record('s) month, for keeping up with the current month calculations
	-> Some parameters are imported from defineconstants.py file in the same folder as this file.
	-> These parameters serve as constants used in the calculation for the new parameters to be saved in the current day's record.
	-> Daily, monthly and yearly calculations are carried out as shown in the Sheets/Solar_Exception_Report.xlsx
	-> All the variables are stored as Decimal type. It makes calculation easier, and no need of more type-casting when calculating other intermediate variables.
"""




class Panipat_SheetAdmin(admin.ModelAdmin):
	list_filter = (('date',DateRangeFilter), )
	date_hierarchy = 'date'
	ordering = ('-date',)
	actions_on_top = True 	#so that the action changelist bar displays on the top
	actions_on_bottom = True 	#so that the action changelist bar displays on the bottom
	empty_value_display = '-empty-'
	list_max_show_all = 366
	readonly_fields = (
						'monthly_target_generation',
						'monthly_actual_generation',
						'yearly_target_generation',
						'yearly_actual_generation',
						'daily_target_plf',
						'monthly_target_plf',
						'yearly_target_plf',
						'daily_actual_plf',
						'monthly_actual_plf',
						'yearly_actual_plf',
						'monthly_target_irradiance',
						'monthly_actual_irradiance',
						'yearly_target_irradiance',
						'yearly_actual_irradiance',
						'daily_target_performance_ratio',
						'monthly_target_performance_ratio',
						'yearly_target_performance_ratio',
						'daily_actual_performance_ratio',
						'monthly_actual_performance_ratio',
						'yearly_actual_performance_ratio',
						'daily_irradiance_loss',
						'monthly_irradiance_loss',
						'yearly_irradiance_loss',
						'daily_deemed_loss_plf',
						'monthly_deemed_loss_plf',
						'yearly_deemed_loss_plf',
						'monthly_deemed_loss',
						'yearly_deemed_loss',
						'daily_grid_loss_plf',
						'monthly_grid_loss_plf', 
						'yearly_grid_loss_plf',
						'monthly_grid_loss',
						'yearly_grid_loss',
						'monthly_bd_loss',
						'yearly_bd_loss',
						'daily_bd_loss_plf',
						'monthly_bd_loss_plf',
						'yearly_bd_loss_plf',
						'monthly_dust_loss',
						'yearly_dust_loss',
						'daily_dust_loss_plf',
						'monthly_dust_loss_plf',
						'yearly_dust_loss_plf',
						'daily_misc_loss',
						'monthly_misc_loss',
						'yearly_misc_loss',
			)
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh) [Operator Entry: Daily Irradiation Target PLF(enter the combined for both sites)]', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh) [Operator Entry: Daily Target Generation]', {
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
		('Target & Actual Irradiance [Operator Entry: Daily Actual Irradiance,]', {
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
		('Deemed Loss (Operator Entry: Daily Deemed Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to grid outage (Operator Entry: Daily Grid Outage Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown (Operator Entry: Daily BreakDown Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss (Operator Entry: Daily Dust Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
		('Today Major Observations (Separate the observations by ",")', {
				'fields': (('major_observations',),)
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
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
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
			
			#rounding the final answer coming out of calculation at 2 decimal places
			#this value is used for irradiation_sum
			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)


			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(panipat_constant*24))*100))
			obj.daily_target_performance_ratio = Decimal(str((float(obj.daily_target_generation)/(float(obj.daily_target_irradiance)*panipat_constant))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*panipat_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(panipat_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(panipat_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(panipat_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(panipat_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_target_generation = Decimal(str(float(obj.daily_target_generation)*day))
			obj.monthly_target_performance_ratio = obj.daily_target_performance_ratio
			obj.monthly_actual_irradiance = Decimal(str((((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance)  if obj.daily_actual_irradiance>0 else 0))/float(day))))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*panipat_constant*(float(day))))*100))
			obj.monthly_target_plf = Decimal(str((float(obj.monthly_target_generation)/(panipat_constant*24*day))*100))
			obj.monthly_target_irradiance = obj.daily_target_irradiance
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + ((float(obj.daily_actual_irradiance) if obj.daily_actual_irradiance>0 else 0))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
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
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_generation
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(panipat_constant*24*(float(obj.days_elapsed))))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/float(obj.days_elapsed)))
			obj.yearly_target_performance_ratio = Decimal(str((float(obj.yearly_target_generation)/(float(obj.yearly_target_irradiance)*float(obj.days_elapsed)*castamet_constant))*100))
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(panipat_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(panipat_constant*24*float(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(panipat_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(panipat_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(panipat_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(panipat_constant*24*float(obj.days_elapsed)))*100))
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
	readonly_fields = (
						'monthly_target_generation',
						'monthly_actual_generation',
						'yearly_target_generation',
						'yearly_actual_generation',
						'daily_target_plf',
						'monthly_target_plf',
						'yearly_target_plf',
						'daily_actual_plf',
						'monthly_actual_plf',
						'yearly_actual_plf',
						'monthly_target_irradiance',
						'monthly_actual_irradiance',
						'yearly_target_irradiance',
						'yearly_actual_irradiance',
						'daily_target_performance_ratio',
						'monthly_target_performance_ratio',
						'yearly_target_performance_ratio',
						'daily_actual_performance_ratio',
						'monthly_actual_performance_ratio',
						'yearly_actual_performance_ratio',
						'daily_irradiance_loss',
						'monthly_irradiance_loss',
						'yearly_irradiance_loss',
						'daily_deemed_loss_plf',
						'monthly_deemed_loss_plf',
						'yearly_deemed_loss_plf',
						'monthly_deemed_loss',
						'yearly_deemed_loss',
						'daily_grid_loss_plf',
						'monthly_grid_loss_plf', 
						'yearly_grid_loss_plf',
						'monthly_grid_loss',
						'yearly_grid_loss',
						'monthly_bd_loss',
						'yearly_bd_loss',
						'daily_bd_loss_plf',
						'monthly_bd_loss_plf',
						'yearly_bd_loss_plf',
						'monthly_dust_loss',
						'yearly_dust_loss',
						'daily_dust_loss_plf',
						'monthly_dust_loss_plf',
						'yearly_dust_loss_plf',
						'daily_misc_loss',
						'monthly_misc_loss',
						'yearly_misc_loss',
			)
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh) [Operator Entry: Daily Irradiation Target PLF(enter the combined for both sites)]', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh) [Operator Entry: Daily Target Generation]', {
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
		('Target & Actual Irradiance [Operator Entry: Daily Actual Irradiance,]', {
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
		('Deemed Loss (Operator Entry: Daily Deemed Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to grid outage (Operator Entry: Daily Grid Outage Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown (Operator Entry: Daily BreakDown Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss (Operator Entry: Daily Dust Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
		('Today Major Observations (Separate the observations by ",")', {
				'fields': (('major_observations',),)
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
			last_record = Castamet_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
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
			irradiation_sum = (float(yearly_tg_till_date)/(castamet_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*castamet_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(castamet_constant*24))*100))
			obj.daily_target_performance_ratio = Decimal(str((float(obj.daily_target_generation)/(float(obj.daily_target_irradiance)*castamet_constant))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*castamet_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(castamet_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(castamet_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(castamet_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(castamet_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_target_generation = Decimal(str(float(obj.daily_target_generation)*day))
			obj.monthly_target_plf = Decimal(str((float(obj.monthly_target_generation)/(panipat_constant*24*day))*100))
			obj.monthly_target_irradiance = obj.daily_target_irradiance
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance)  if obj.daily_actual_irradiance>0 else 0))/float(day)))
			obj.monthly_target_performance_ratio = obj.daily_target_performance_ratio
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*castamet_constant*(day)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(castamet_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(castamet_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(castamet_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(castamet_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_generation
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(castamet_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/float(obj.days_elapsed)))
			obj.yearly_target_performance_ratio = Decimal(str((float(obj.yearly_target_generation)/(float(obj.yearly_target_irradiance)*float(obj.days_elapsed)*castamet_constant))*100))
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/float(obj.days_elapsed))))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(castamet_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(castamet_constant*24*float(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(castamet_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(castamet_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(castamet_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(castamet_constant*24*float(obj.days_elapsed)))*100))
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
	readonly_fields = (
						'monthly_target_generation',
						'monthly_actual_generation',
						'yearly_target_generation',
						'yearly_actual_generation',
						'daily_target_plf',
						'monthly_target_plf',
						'yearly_target_plf',
						'daily_actual_plf',
						'monthly_actual_plf',
						'yearly_actual_plf',
						'monthly_target_irradiance',
						'monthly_actual_irradiance',
						'yearly_target_irradiance',
						'yearly_actual_irradiance',
						'daily_target_performance_ratio',
						'monthly_target_performance_ratio',
						'yearly_target_performance_ratio',
						'daily_actual_performance_ratio',
						'monthly_actual_performance_ratio',
						'yearly_actual_performance_ratio',
						'daily_irradiance_loss',
						'monthly_irradiance_loss',
						'yearly_irradiance_loss',
						'daily_deemed_loss_plf',
						'monthly_deemed_loss_plf',
						'yearly_deemed_loss_plf',
						'monthly_deemed_loss',
						'yearly_deemed_loss',
						'daily_grid_loss_plf',
						'monthly_grid_loss_plf', 
						'yearly_grid_loss_plf',
						'monthly_grid_loss',
						'yearly_grid_loss',
						'monthly_bd_loss',
						'yearly_bd_loss',
						'daily_bd_loss_plf',
						'monthly_bd_loss_plf',
						'yearly_bd_loss_plf',
						'monthly_dust_loss',
						'yearly_dust_loss',
						'daily_dust_loss_plf',
						'monthly_dust_loss_plf',
						'yearly_dust_loss_plf',
						'daily_misc_loss',
						'monthly_misc_loss',
						'yearly_misc_loss',
			)
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh) [Operator Entry: Daily Irradiation Target PLF(enter the combined for both sites)]', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh) [Operator Entry: Daily Target Generation]', {
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
		('Target & Actual Irradiance [Operator Entry: Daily Actual Irradiance,]', {
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
		('Deemed Loss (Operator Entry: Daily Deemed Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to grid outage (Operator Entry: Daily Grid Outage Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown (Operator Entry: Daily BreakDown Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss (Operator Entry: Daily Dust Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
		('Today Major Observations (Separate the observations by ",")', {
				'fields': (('major_observations',),)
			}),
	)

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
			last_record = Jharkhand_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
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
			irradiation_sum = (float(yearly_tg_till_date)/(jharkhand_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*jharkhand_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(jharkhand_constant*24))*100))
			obj.daily_target_performance_ratio = Decimal(str((float(obj.daily_target_generation)/(float(obj.daily_target_irradiance)*jharkhand_constant))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*jharkhand_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(jharkhand_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(jharkhand_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(jharkhand_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(jharkhand_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_target_generation = Decimal(str(float(obj.daily_target_generation)*day))
			obj.monthly_target_plf = Decimal(str((float(obj.monthly_target_generation)/(panipat_constant*24*day))*100))
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_target_performance_ratio = obj.daily_target_performance_ratio
			obj.monthly_target_irradiance = obj.daily_target_irradiance
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*jharkhand_constant*float(day)))*100))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*jharkhand_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(jharkhand_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(jharkhand_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(jharkhand_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(jharkhand_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_generation
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(jharkhand_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(jharkhand_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(jharkhand_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(jharkhand_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(jharkhand_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(jharkhand_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(jharkhand_constant*24*float(obj.days_elapsed)))*100))
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
	readonly_fields = (
						'monthly_target_generation',
						'monthly_actual_generation',
						'yearly_target_generation',
						'yearly_actual_generation',
						'daily_target_plf',
						'monthly_target_plf',
						'yearly_target_plf',
						'daily_actual_plf',
						'monthly_actual_plf',
						'yearly_actual_plf',
						'monthly_target_irradiance',
						'monthly_actual_irradiance',
						'yearly_target_irradiance',
						'yearly_actual_irradiance',
						'daily_target_performance_ratio',
						'monthly_target_performance_ratio',
						'yearly_target_performance_ratio',
						'daily_actual_performance_ratio',
						'monthly_actual_performance_ratio',
						'yearly_actual_performance_ratio',
						'daily_irradiance_loss',
						'monthly_irradiance_loss',
						'yearly_irradiance_loss',
						'daily_deemed_loss_plf',
						'monthly_deemed_loss_plf',
						'yearly_deemed_loss_plf',
						'monthly_deemed_loss',
						'yearly_deemed_loss',
						'daily_grid_loss_plf',
						'monthly_grid_loss_plf', 
						'yearly_grid_loss_plf',
						'monthly_grid_loss',
						'yearly_grid_loss',
						'monthly_bd_loss',
						'yearly_bd_loss',
						'daily_bd_loss_plf',
						'monthly_bd_loss_plf',
						'yearly_bd_loss_plf',
						'monthly_dust_loss',
						'yearly_dust_loss',
						'daily_dust_loss_plf',
						'monthly_dust_loss_plf',
						'yearly_dust_loss_plf',
						'daily_misc_loss',
						'monthly_misc_loss',
						'yearly_misc_loss',
			)
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh) [Operator Entry: Daily Irradiation Target PLF(enter the combined for both sites)]', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh) [Operator Entry: Daily Target Generation]', {
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
		('Target & Actual Irradiance [Operator Entry: Daily Actual Irradiance,]', {
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
		('Deemed Loss (Operator Entry: Daily Deemed Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to grid outage (Operator Entry: Daily Grid Outage Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown (Operator Entry: Daily BreakDown Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss (Operator Entry: Daily Dust Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
		('Today Major Observations (Separate the observations by ",")', {
				'fields': (('major_observations',),)
			}),
	)

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
			last_record = Roorkee_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss


			else:
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
			irradiation_sum = (float(yearly_tg_till_date)/(roorkee_constant*24*(float(obj.days_elapsed)-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*panipat_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(roorkee_constant*24))*100))
			obj.daily_target_performance_ratio = Decimal(str((float(obj.daily_target_generation)/(float(obj.daily_target_irradiance)*roorkee_constant))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*roorkee_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(roorkee_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(roorkee_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(roorkee_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(roorkee_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_target_generation = Decimal(str(float(obj.daily_target_generation)*day))
			obj.monthly_actual_irradiance = Decimal(str(((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_target_performance_ratio = obj.daily_target_performance_ratio	#change
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*roorkee_constant*(float(obj.days_elapsed))))*100))
			obj.monthly_target_plf = Decimal(str((float(obj.monthly_target_generation)/(panipat_constant*24*day))*100))
			obj.monthly_target_irradiance = obj.daily_target_irradiance
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(roorkee_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss+ Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(roorkee_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(roorkee_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(roorkee_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_generation
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(roorkee_constant*24*obj.days_elapsed))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/(obj.days_elapsed)))
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(roorkee_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(roorkee_constant*24*(obj.days_elapsed)))*100 - 0.1))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(roorkee_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(roorkee_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(roorkee_constant*24*(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(roorkee_constant*24*(obj.days_elapsed)))*100))
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
	readonly_fields = (
						'monthly_target_generation',
						'monthly_actual_generation',
						'yearly_target_generation',
						'yearly_actual_generation',
						'daily_target_plf',
						'monthly_target_plf',
						'yearly_actual_irradiance',
						'daily_target_performance_ratio',
						'monthly_target_performance_ratio',
						'yearly_target_performance_ratio',
						'daily_actual_performance_ratio',
						'monthly_actual_performance_ratio',
						'yearly_actual_performance_ratio',
						'daily_irradiance_loss',
						'monthly_irradiance_loss',
						'yearly_irradiance_loss',
						'daily_deemed_loss_plf',
						'monthly_deemed_loss_plf',
						'yearly_deemed_loss_plf',
						'monthly_deemed_loss',
						'yearly_deemed_loss',
						'yearly_target_plf',
						'daily_actual_plf',
						'monthly_actual_plf',
						'yearly_actual_plf',
						'monthly_target_irradiance',
						'monthly_actual_irradiance',
						'yearly_target_irradiance',
						'daily_grid_loss_plf',
						'monthly_grid_loss_plf', 
						'yearly_grid_loss_plf',
						'monthly_grid_loss',
						'yearly_grid_loss',
						'monthly_bd_loss',
						'yearly_bd_loss',
						'daily_bd_loss_plf',
						'monthly_bd_loss_plf',
						'yearly_bd_loss_plf',
						'monthly_dust_loss',
						'yearly_dust_loss',
						'daily_dust_loss_plf',
						'monthly_dust_loss_plf',
						'yearly_dust_loss_plf',
						'daily_misc_loss',
						'monthly_misc_loss',
						'yearly_misc_loss',
			)
	fieldsets = (
		(None, {
				'fields': ('days_elapsed',)
			}),
		('Target PLF Operator Entry (in kWh) [Operator Entry: Daily Irradiation Target PLF(enter the combined for both sites)]', {
				'fields': (('irradiation_target_plf', 'kwh_target_plf'),)
			}),
		('Target & Actual Generation (in kWh) [Operator Entry: Daily Target Generation]', {
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
		('Target & Actual Irradiance [Operator Entry: Daily Actual Irradiance,]', {
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
		('Deemed Loss (Operator Entry: Daily Deemed Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_deemed_loss', 'monthly_deemed_loss', 'yearly_deemed_loss'),
					('daily_deemed_loss_plf', 'monthly_deemed_loss_plf', 'yearly_deemed_loss_plf'),
				)
			}),
		('Loss due to grid outage (Operator Entry: Daily Grid Outage Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_grid_loss', 'monthly_grid_loss', 'yearly_grid_loss'),
					('daily_grid_loss_plf', 'monthly_grid_loss_plf', 'yearly_grid_loss_plf'),
				)
			}),
		('Loss due to BreakDown (Operator Entry: Daily BreakDown Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_bd_loss', 'monthly_bd_loss', 'yearly_bd_loss'),
					('daily_bd_loss_plf', 'monthly_bd_loss_plf', 'yearly_bd_loss_plf'),
				)
			}),
		('Dust loss (Operator Entry: Daily Dust Loss, PLFs will be calculated accordingly)', {
				'fields': (
					('daily_dust_loss', 'monthly_dust_loss', 'yearly_dust_loss'),
					('daily_dust_loss_plf', 'monthly_dust_loss_plf', 'yearly_dust_loss_plf'),
				)
			}),
		('Miscellaneous Loss', {
				'fields': (('daily_misc_loss', 'monthly_misc_loss', 'yearly_misc_loss'),)
			}),
		('Today Major Observations (Separate the observations by ",")', {
				'fields': (('major_observations',),)
			}),
	)

	def save_model(self, request, obj, form, change):
		monthly_actual_performance_ratio_till_date = 0.0
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
			last_record = Beawar_Sheet.objects.latest('date')
			last_record_month = int(last_record.date[3:5])

			if last_record_month == month:
				month_irradiance_till_date = last_record.monthly_actual_irradiance
				monthly_deemedloss_till_date = last_record.monthly_deemed_loss
				monthly_gridloss_till_date = last_record.monthly_grid_loss
				monthly_bdloss_till_date = last_record.monthly_bd_loss
				monthly_dustloss_till_date = last_record.monthly_dust_loss
				monthly_actual_performance_ratio_till_date = last_record.monthly_actual_performance_ratio
				monthly_irradiance_loss_till_date = last_record.monthly_actual_irradiance


			else:
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
			irradiation_sum = (float(yearly_tg_till_date)/(beawar_constant*24*(obj.days_elapsed-1)))*100 - yearly_irradianceloss_till_date - 0.1

			if irradiation_sum < 0.0:
				irradiation_sum = 0.0

		except:
			pass


		if form.has_changed():
			# obj.kwh_target_plf = obj.irradiation_target_plf

			obj.kwh_target_plf = round((float(obj.irradiation_target_plf)*beawar_constant*24)/100, 2)
			irradiation_sum = irradiation_sum + float(obj.kwh_target_plf)

			#Calculation of daily parameters
			obj.daily_target_plf = Decimal(str(((float(obj.daily_target_generation))/(beawar_constant*24))*100))
			obj.daily_target_performance_ratio = Decimal(str((float(obj.daily_target_generation)/(float(obj.daily_target_irradiance)*beawar_constant))*100))
			obj.daily_actual_performance_ratio = Decimal(str(((float(obj.daily_actual_generation))/(float(obj.daily_actual_irradiance)*beawar_constant))*100))
			obj.daily_irradiance_loss = Decimal(str(obj.daily_target_plf)) - obj.irradiation_target_plf
			obj.daily_deemed_loss_plf = Decimal(str(((float(obj.daily_deemed_loss))/(beawar_constant*24))*100))
			obj.daily_grid_loss_plf = Decimal(str(((float(obj.daily_grid_loss))/(beawar_constant*24))*100))
			obj.daily_bd_loss_plf = Decimal(str(((float(obj.daily_bd_loss))/(beawar_constant*24))*100))
			obj.daily_dust_loss_plf = Decimal(str(((float(obj.daily_dust_loss))/(beawar_constant*24))*100))
			daily_generation_loss = obj.daily_target_plf - obj.daily_actual_plf
			obj.daily_misc_loss = daily_generation_loss - obj.daily_irradiance_loss - obj.daily_deemed_loss_plf - obj.daily_grid_loss_plf - obj.daily_bd_loss_plf - obj.daily_dust_loss_plf


			#Calculation of monthly parameters
			obj.monthly_target_generation = Decimal(str(float(obj.daily_target_generation)*day))
			obj.monthly_target_plf = Decimal(str((float(obj.monthly_target_generation)/(panipat_constant*24*day))*100))
			obj.monthly_target_irradiance = obj.daily_target_irradiance
			obj.monthly_actual_irradiance = Decimal(str((((float(day) - 1)*(float(month_irradiance_till_date)) + (float(obj.daily_actual_irradiance)  if obj.daily_actual_irradiance>0 else 0))/float(day))))
			obj.monthly_target_performance_ratio = obj.daily_target_performance_ratio
			obj.monthly_actual_performance_ratio = Decimal(str(((float(day) - 1)*(float(monthly_actual_performance_ratio_till_date)) + (float(obj.daily_actual_performance_ratio))/float(day))))
			monthly_mean_target_irradiation = Decimal(str(((float(day) - 1)*(float(monthly_irradiance_loss_till_date)) + (float(obj.daily_actual_irradiance))/float(day))))
			obj.monthly_irradiance_loss = obj.monthly_target_plf - Decimal(str(monthly_mean_target_irradiation))
			obj.monthly_actual_performance_ratio = Decimal(str(((float(obj.monthly_actual_generation))/(float(obj.monthly_actual_irradiance)*beawar_constant))*100))
			obj.monthly_deemed_loss = obj.daily_deemed_loss + Decimal(str(monthly_deemedloss_till_date))
			obj.monthly_deemed_loss_plf = Decimal(str(((float(obj.monthly_deemed_loss))/(beawar_constant*24*day))*100))
			obj.monthly_grid_loss = obj.daily_grid_loss + Decimal(str(monthly_gridloss_till_date))
			obj.monthly_grid_loss_plf = Decimal(str(((float(obj.monthly_grid_loss))/(beawar_constant*24*day))*100))
			obj.monthly_bd_loss = Decimal(str(monthly_bdloss_till_date)) + obj.daily_bd_loss
			obj.monthly_bd_loss_plf = Decimal(str(((float(obj.monthly_bd_loss))/(beawar_constant*24*day))*100))
			obj.monthly_dust_loss = Decimal(str(monthly_dustloss_till_date)) + obj.daily_dust_loss
			obj.monthly_dust_loss_plf = Decimal(str(((float(obj.monthly_dust_loss))/(beawar_constant*24*day))*100))
			monthly_generation_loss = obj.monthly_target_plf - obj.monthly_actual_plf
			obj.monthly_misc_loss = monthly_generation_loss - obj.monthly_irradiance_loss - obj.monthly_deemed_loss_plf - obj.monthly_grid_loss_plf - obj.monthly_bd_loss_plf - obj.monthly_dust_loss_plf


			#Calculation of Yearly Parameters
			obj.yearly_target_generation = Decimal(str(yearly_target_gen_till_date)) + obj.daily_target_generation
			obj.yearly_target_plf = Decimal(str(((float(obj.yearly_target_generation))/(beawar_constant*24*(float(obj.days_elapsed))))*100))
			obj.yearly_actual_irradiance = Decimal(str(((float(obj.days_elapsed)-1)*(float(annual_actual_irradiance_till_date)) + (float(obj.daily_actual_irradiance)))/float(obj.days_elapsed))) + 0.1
			
			obj.yearly_target_performance_ratio = Decimal(str((float(obj.yearly_target_generation)/(float(obj.yearly_target_irradiance)*beawar_constant*float(obj.days_elapsed)))*100))
			irradiation_sum = Decimal(str(((irradiation_sum*(obj.days_elapsed-1) + float(obj.kwh_target_plf))/obj.days_elapsed)))
			obj.yearly_irradiance_loss = Decimal(str((float(obj.yearly_target_generation)/(beawar_constant*24*(obj.days_elapsed)))*100 - (float(irradiation_sum)/(beawar_constant*24*float(obj.days_elapsed)))*100))
			yearly_generation_loss = obj.yearly_target_plf - obj.yearly_actual_plf
			obj.yearly_deemed_loss = Decimal(str(yearly_deemedloss_till_date)) + obj.daily_deemed_loss_plf
			obj.yearly_deemed_loss_plf = Decimal(str((float(obj.yearly_deemed_loss)/(beawar_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_grid_loss = Decimal(str(yearly_gridloss_till_date)) + obj.daily_grid_loss
			obj.yearly_grid_loss_plf = Decimal(str((float(obj.yearly_grid_loss)/(beawar_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_bd_loss = Decimal(str(yearly_bdloss_till_date)) + obj.daily_bd_loss
			obj.yearly_bd_loss_plf = Decimal(str((float(obj.yearly_bd_loss)/(beawar_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_dust_loss = Decimal(str(yearly_dustloss_till_date)) + obj.daily_dust_loss
			obj.yearly_dust_loss_plf = Decimal(str((float(obj.yearly_dust_loss)/(beawar_constant*24*float(obj.days_elapsed)))*100))
			obj.yearly_misc_loss = yearly_generation_loss - obj.yearly_irradiance_loss - obj.yearly_deemed_loss_plf - obj.yearly_grid_loss_plf - obj.yearly_bd_loss_plf - obj.yearly_dust_loss_plf


		super().save_model(request, obj, form, change)




	# form = EntryForm

admin.site.register(Beawar_Sheet, Beawar_SheetAdmin)

# @admin.register(Operator_Entry)
# class Operator_EntryAdmin(admin.ModelAdmin):
# 	pass