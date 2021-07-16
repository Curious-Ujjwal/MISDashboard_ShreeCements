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


class Panipat_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	daily_target_generation = models.PositiveIntegerField(default=0)
	daily_actual_generation = models.PositiveIntegerField(default=0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.PositiveIntegerField(default=0)
	monthly_actual_generation = models.PositiveIntegerField(default=0)
	yearly_target_generation = models.PositiveIntegerField(default=0)
	yearly_actual_generation = models.PositiveIntegerField(default=0)
	daily_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Actual PLF(%)')
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
	daily_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Low Irradiance')
	monthly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Low Irradiance')
	yearly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Low Irradiance')
	daily_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Deemed')
	monthly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Deemed')
	yearly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Deemed')
	daily_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss sue to GRID outage')
	monthly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss sue to GRID outage')
	yearly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss sue to GRID outage')
	daily_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to BD')
	monthly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to BD')
	yearly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to BD')
	daily_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Dust')
	monthly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Dust')
	yearly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Dust')
	daily_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Misc. Losses')
	monthly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Misc. Losses')
	yearly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Misc. Losses')
	
	# planning of a field for operator entries as follows:
	# 1-> make some operator entry char fields -- DONE
	# 2-> and a form to select those fields -- DONE
	# 3-> write a function in admin so that when user clicks on those options in 1) then browser prompts and ask for the observation
	# 4-> take the i/p and save that as the value and the placeholder in the select
	# 5-> update the entries in the form below those options to select those things
	# 6-> write another function to save them in the respective sheet
	# operator_entries = models.ManyToManyField(Operator_Entry, blank=True, editable=True)

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Castamet_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	daily_target_generation = models.PositiveIntegerField(default=0)
	daily_actual_generation = models.PositiveIntegerField(default=0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.PositiveIntegerField(default=0)
	monthly_actual_generation = models.PositiveIntegerField(default=0)
	yearly_target_generation = models.PositiveIntegerField(default=0)
	yearly_actual_generation = models.PositiveIntegerField(default=0)
	daily_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Actual PLF(%)')
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
	daily_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Low Irradiance')
	monthly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Low Irradiance')
	yearly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Low Irradiance')
	daily_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Deemed')
	monthly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Deemed')
	yearly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Deemed')
	daily_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss sue to GRID outage')
	monthly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss sue to GRID outage')
	yearly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss sue to GRID outage')
	daily_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to BD')
	monthly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to BD')
	yearly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to BD')
	daily_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Dust')
	monthly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Dust')
	yearly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Dust')
	daily_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Misc. Losses')
	monthly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Misc. Losses')
	yearly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Misc. Losses')
	
	# planning of a field for operator entries as follows:
	# 1-> make some operator entry char fields -- DONE
	# 2-> and a form to select those fields -- DONE
	# 3-> write a function in admin so that when user clicks on those options in 1) then browser prompts and ask for the observation
	# 4-> take the i/p and save that as the value and the placeholder in the select
	# 5-> update the entries in the form below those options to select those things
	# 6-> write another function to save them in the respective sheet
	# operator_entries = models.ManyToManyField(Operator_Entry, blank=True, editable=True)

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Jharkhand_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	daily_target_generation = models.PositiveIntegerField(default=0)
	daily_actual_generation = models.PositiveIntegerField(default=0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.PositiveIntegerField(default=0)
	monthly_actual_generation = models.PositiveIntegerField(default=0)
	yearly_target_generation = models.PositiveIntegerField(default=0)
	yearly_actual_generation = models.PositiveIntegerField(default=0)
	daily_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Actual PLF(%)')
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
	daily_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Low Irradiance')
	monthly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Low Irradiance')
	yearly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Low Irradiance')
	daily_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Deemed')
	monthly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Deemed')
	yearly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Deemed')
	daily_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss sue to GRID outage')
	monthly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss sue to GRID outage')
	yearly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss sue to GRID outage')
	daily_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to BD')
	monthly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to BD')
	yearly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to BD')
	daily_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Dust')
	monthly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Dust')
	yearly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Dust')
	daily_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Misc. Losses')
	monthly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Misc. Losses')
	yearly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Misc. Losses')
	
	# planning of a field for operator entries as follows:
	# 1-> make some operator entry char fields -- DONE
	# 2-> and a form to select those fields -- DONE
	# 3-> write a function in admin so that when user clicks on those options in 1) then browser prompts and ask for the observation
	# 4-> take the i/p and save that as the value and the placeholder in the select
	# 5-> update the entries in the form below those options to select those things
	# 6-> write another function to save them in the respective sheet
	# operator_entries = models.ManyToManyField(Operator_Entry, blank=True, editable=True)

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Roorkee_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	daily_target_generation = models.PositiveIntegerField(default=0)
	daily_actual_generation = models.PositiveIntegerField(default=0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.PositiveIntegerField(default=0)
	monthly_actual_generation = models.PositiveIntegerField(default=0)
	yearly_target_generation = models.PositiveIntegerField(default=0)
	yearly_actual_generation = models.PositiveIntegerField(default=0)
	daily_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Actual PLF(%)')
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
	daily_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Low Irradiance')
	monthly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Low Irradiance')
	yearly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Low Irradiance')
	daily_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Deemed')
	monthly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Deemed')
	yearly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Deemed')
	daily_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss sue to GRID outage')
	monthly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss sue to GRID outage')
	yearly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss sue to GRID outage')
	daily_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to BD')
	monthly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to BD')
	yearly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to BD')
	daily_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Dust')
	monthly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Dust')
	yearly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Dust')
	daily_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Misc. Losses')
	monthly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Misc. Losses')
	yearly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Misc. Losses')
	
	# planning of a field for operator entries as follows:
	# 1-> make some operator entry char fields -- DONE
	# 2-> and a form to select those fields -- DONE
	# 3-> write a function in admin so that when user clicks on those options in 1) then browser prompts and ask for the observation
	# 4-> take the i/p and save that as the value and the placeholder in the select
	# 5-> update the entries in the form below those options to select those things
	# 6-> write another function to save them in the respective sheet
	# operator_entries = models.ManyToManyField(Operator_Entry, blank=True, editable=True)

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate


class Beawar_Sheet(models.Model):
	date = models.DateField(default=date.today, editable=False, primary_key=True)
	daily_target_generation = models.PositiveIntegerField(default=0)
	daily_actual_generation = models.PositiveIntegerField(default=0)
	irradiation_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual Irradiation')
	kwh_target_plf = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Target PLF based on Actual KWH')
	monthly_target_generation = models.PositiveIntegerField(default=0)
	monthly_actual_generation = models.PositiveIntegerField(default=0)
	yearly_target_generation = models.PositiveIntegerField(default=0)
	yearly_actual_generation = models.PositiveIntegerField(default=0)
	daily_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Target PLF(%)')
	daily_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Actual PLF(%)')
	monthly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Target PLF(%)')
	monthly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Actual PLF(%)')
	yearly_target_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Target PLF(%)')
	yearly_actual_plf = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Actual PLF(%)')
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
	daily_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Low Irradiance')
	monthly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Low Irradiance')
	yearly_irradiance_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Low Irradiance')
	daily_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Deemed')
	monthly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Deemed')
	yearly_deemed_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Deemed')
	daily_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss sue to GRID outage')
	monthly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss sue to GRID outage')
	yearly_grid_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss sue to GRID outage')
	daily_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to BD')
	monthly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to BD')
	yearly_bd_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to BD')
	daily_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Loss due to Dust')
	monthly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Montlhy Loss due to Dust')
	yearly_dust_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Loss due to Dust')
	daily_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Daily Misc. Losses')
	monthly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Monthly Misc. Losses')
	yearly_misc_loss = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Yearly Misc. Losses')
	
	# planning of a field for operator entries as follows:
	# 1-> make some operator entry char fields -- DONE
	# 2-> and a form to select those fields -- DONE
	# 3-> write a function in admin so that when user clicks on those options in 1) then browser prompts and ask for the observation
	# 4-> take the i/p and save that as the value and the placeholder in the select
	# 5-> update the entries in the form below those options to select those things
	# 6-> write another function to save them in the respective sheet
	# operator_entries = models.ManyToManyField(Operator_Entry, blank=True, editable=True)

	class Meta:
		ordering = ['date']

	def __str__(self):
		cdate = f"{self.date}"
		cdate = "-".join(reversed(cdate.split("-")))
		return cdate
