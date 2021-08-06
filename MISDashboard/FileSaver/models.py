from django.db import models
from datetime import date
import ast

OBSERVATION_CHOICES = (
	("Choice-1", "Choice-1"),
	("Choice-2", "Choice-2"),
	("Choice-3", "Choice-3"),
	("Choice-4", "Choice-4"),
	("Choice-5", "Choice-5"),
	("Choice-6", "Choice-6"),
	("Choice-7", "Choice-7"),
)

class Operator_Entry(models.Model):
	entry = models.TextField(max_length=20, choices=OBSERVATION_CHOICES, default='Choice-2', editable=True)

	def __str__(self):
		return 'Operator-Entry'+f"{self.pk}"

"""
	Structure for Panipat_Sheet, Castamet_Sheet, Jharkhand_Sheet, Roorkee_Sheet, Beawar_Sheet
	-> date : date of the month 	D M Y
	-> days_elapsed : days that have passed in the running year
	-> parameters for the target, actual values are assigned for 
		Daily, Monhly, and Yearly generation or loss values
"""


class Panipat_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	days_elapsed = models.PositiveIntegerField(default=1, verbose_name='No. of days elapsed from the start of the year', help_text='Start of the year is marked by April of that session.')
	daily_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	monthly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Actual PLF(%)')
	daily_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Performance Ratio(PR)')
	daily_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Performance Ratio(PR)')
	monthly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Performance Ratio(PR)')
	monthly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Performance Ratio(PR)')
	yearly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Performance Ratio(PR)')
	yearly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Performance Ratio(PR)')
	daily_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Irradiance(Inclined)')
	daily_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Irradiance(Inclined)')
	monthly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Irradiance(Inclined)')
	monthly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Irradiance(Inclined)')
	yearly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Irradiance(Inclined)')
	yearly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Irradiance(Inclined)')
	daily_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Low Irradiance(in %)')
	monthly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Low Irradiance(in %)')
	yearly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Low Irradiance(in %)')
	daily_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in kWh)')
	monthly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in kWh)')
	yearly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in kWh)')
	daily_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in %)')
	monthly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in %)')
	yearly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in %)')
	daily_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in kWh)')
	monthly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in kWh)')
	yearly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in kWh)')
	daily_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in %)')
	monthly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in %)')
	yearly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in %)')
	daily_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in kWh)')
	monthly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in kWh)')
	yearly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in kWh)')
	daily_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in %)')
	monthly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in %)')
	yearly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in %)')
	daily_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in kWh)')
	monthly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in kWh)')
	yearly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in kWh)')
	daily_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in %)')
	monthly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in %)')
	yearly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in %)')
	daily_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Misc. Losses(in %)')
	monthly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Monthly Misc. Losses(in %)')
	yearly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Misc. Losses(in %)')
	major_observations = models.TextField(verbose_name='Today Major Observations', default='')

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate



class Castamet_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	days_elapsed = models.PositiveIntegerField(default=1, verbose_name='No. of days elapsed from the start of the year', help_text='Start of the year is marked by April of that session.')
	daily_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	monthly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Actual PLF(%)')
	daily_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Performance Ratio(PR)')
	daily_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Performance Ratio(PR)')
	monthly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Performance Ratio(PR)')
	monthly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Performance Ratio(PR)')
	yearly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Performance Ratio(PR)')
	yearly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Performance Ratio(PR)')
	daily_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Irradiance(Inclined)')
	daily_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Irradiance(Inclined)')
	monthly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Irradiance(Inclined)')
	monthly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Irradiance(Inclined)')
	yearly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Irradiance(Inclined)')
	yearly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Irradiance(Inclined)')
	daily_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Low Irradiance(in %)')
	monthly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Low Irradiance(in %)')
	yearly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Low Irradiance(in %)')
	daily_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in kWh)')
	monthly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in kWh)')
	yearly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in kWh)')
	daily_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in %)')
	monthly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in %)')
	yearly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in %)')
	daily_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in kWh)')
	monthly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in kWh)')
	yearly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in kWh)')
	daily_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in %)')
	monthly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in %)')
	yearly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in %)')
	daily_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in kWh)')
	monthly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in kWh)')
	yearly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in kWh)')
	daily_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in %)')
	monthly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in %)')
	yearly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in %)')
	daily_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in kWh)')
	monthly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in kWh)')
	yearly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in kWh)')
	daily_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in %)')
	monthly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in %)')
	yearly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in %)')
	daily_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Misc. Losses(in %)')
	monthly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Monthly Misc. Losses(in %)')
	yearly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Misc. Losses(in %)')
	major_observations = models.TextField(verbose_name='Today Major Observations', default='')

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Jharkhand_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	days_elapsed = models.PositiveIntegerField(default=1, verbose_name='No. of days elapsed from the start of the year', help_text='Start of the year is marked by April of that session.')
	daily_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	monthly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Actual PLF(%)')
	daily_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Performance Ratio(PR)')
	daily_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Performance Ratio(PR)')
	monthly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Performance Ratio(PR)')
	monthly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Performance Ratio(PR)')
	yearly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Performance Ratio(PR)')
	yearly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Performance Ratio(PR)')
	daily_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Irradiance(Inclined)')
	daily_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Irradiance(Inclined)')
	monthly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Irradiance(Inclined)')
	monthly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Irradiance(Inclined)')
	yearly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Irradiance(Inclined)')
	yearly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Irradiance(Inclined)')
	daily_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Low Irradiance(in %)')
	monthly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Low Irradiance(in %)')
	yearly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Low Irradiance(in %)')
	daily_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in kWh)')
	monthly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in kWh)')
	yearly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in kWh)')
	daily_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in %)')
	monthly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in %)')
	yearly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in %)')
	daily_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in kWh)')
	monthly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in kWh)')
	yearly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in kWh)')
	daily_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in %)')
	monthly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in %)')
	yearly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in %)')
	daily_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in kWh)')
	monthly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in kWh)')
	yearly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in kWh)')
	daily_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in %)')
	monthly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in %)')
	yearly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in %)')
	daily_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in kWh)')
	monthly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in kWh)')
	yearly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in kWh)')
	daily_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in %)')
	monthly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in %)')
	yearly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in %)')
	daily_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Misc. Losses(in %)')
	monthly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Monthly Misc. Losses(in %)')
	yearly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Misc. Losses(in %)')
	major_observations = models.TextField(verbose_name='Today Major Observations', default='')

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Roorkee_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	days_elapsed = models.PositiveIntegerField(default=1, verbose_name='No. of days elapsed from the start of the year', help_text='Start of the year is marked by April of that session.')
	daily_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	monthly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Actual PLF(%)')
	daily_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Performance Ratio(PR)')
	daily_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Performance Ratio(PR)')
	monthly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Performance Ratio(PR)')
	monthly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Performance Ratio(PR)')
	yearly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Performance Ratio(PR)')
	yearly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Performance Ratio(PR)')
	daily_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Irradiance(Inclined)')
	daily_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Irradiance(Inclined)')
	monthly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Irradiance(Inclined)')
	monthly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Irradiance(Inclined)')
	yearly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Irradiance(Inclined)')
	yearly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Irradiance(Inclined)')
	daily_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Low Irradiance(in %)')
	monthly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Low Irradiance(in %)')
	yearly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Low Irradiance(in %)')
	daily_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in kWh)')
	monthly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in kWh)')
	yearly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in kWh)')
	daily_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in %)')
	monthly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in %)')
	yearly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in %)')
	daily_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in kWh)')
	monthly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in kWh)')
	yearly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in kWh)')
	daily_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in %)')
	monthly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in %)')
	yearly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in %)')
	daily_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in kWh)')
	monthly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in kWh)')
	yearly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in kWh)')
	daily_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in %)')
	monthly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in %)')
	yearly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in %)')
	daily_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in kWh)')
	monthly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in kWh)')
	yearly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in kWh)')
	daily_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in %)')
	monthly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in %)')
	yearly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in %)')
	daily_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Misc. Losses(in %)')
	monthly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Monthly Misc. Losses(in %)')
	yearly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Misc. Losses(in %)')
	major_observations = models.TextField(verbose_name='Today Major Observations', default='')

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Beawar_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	days_elapsed = models.PositiveIntegerField(default=1, verbose_name='No. of days elapsed from the start of the year', help_text='Start of the year is marked by April of that session.')
	daily_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	monthly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_target_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	yearly_actual_generation = models.DecimalField(max_digits=7, decimal_places=2,default=0.0)
	daily_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Yearly Actual PLF(%)')
	daily_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Performance Ratio(PR)')
	daily_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Performance Ratio(PR)')
	monthly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Performance Ratio(PR)')
	monthly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Performance Ratio(PR)')
	yearly_target_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Performance Ratio(PR)')
	yearly_actual_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Performance Ratio(PR)')
	daily_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Target Irradiance(Inclined)')
	daily_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Daily Actual Irradiance(Inclined)')
	monthly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Target Irradiance(Inclined)')
	monthly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Monthly Actual Irradiance(Inclined)')
	yearly_target_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Target Irradiance(Inclined)')
	yearly_actual_irradiance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Yearly Actual Irradiance(Inclined)')
	daily_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Low Irradiance(in %)')
	monthly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Low Irradiance(in %)')
	yearly_irradiance_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Low Irradiance(in %)')
	daily_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in kWh)')
	monthly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in kWh)')
	yearly_deemed_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in kWh)')
	daily_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Deemed(in %)')
	monthly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Deemed(in %)')
	yearly_deemed_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Deemed(in %)')
	daily_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in kWh)')
	monthly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in kWh)')
	yearly_grid_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in kWh)')
	daily_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss sue to GRID outage(in %)')
	monthly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss sue to GRID outage(in %)')
	yearly_grid_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss sue to GRID outage(in %)')
	daily_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in kWh)')
	monthly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in kWh)')
	yearly_bd_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in kWh)')
	daily_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to BD(in %)')
	monthly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to BD(in %)')
	yearly_bd_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to BD(in %)')
	daily_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in kWh)')
	monthly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in kWh)')
	yearly_dust_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in kWh)')
	daily_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Loss due to Dust(in %)')
	monthly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Montlhy Loss due to Dust(in %)')
	yearly_dust_loss_plf = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Loss due to Dust(in %)')
	daily_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Daily Misc. Losses(in %)')
	monthly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Monthly Misc. Losses(in %)')
	yearly_misc_loss = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name='Yearly Misc. Losses(in %)')
	major_observations = models.TextField(verbose_name='Today Major Observations', default='')

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate