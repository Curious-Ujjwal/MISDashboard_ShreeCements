from django.db import models
import date from datetime

# class Beawar_Sheet(models.Model):
# 	date = models.DateField(default=date.today(), editable=False, primary_key=True, input_formats=["%d-%m-%Y"])
# 	generation = models.PositiveIntegerField()
# 	performance_ratio = models.PercentageField(verbose_name='Performance Ratio(PR)')
# 	irradiance = models.DecimalField(max_places=5, decimal_places=2, verbose_name='Irradiance(Inclined)')
# 	irradiance_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Low Irradiance')
# 	deemed_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Deemed')
# 	grid_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss sue to GRID outage')
# 	bd_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to BD')
# 	dust_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Dust')
# 	misc_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Misc. Losses')
# 	major_observations = models.ListTextField(
# 		observation=CharField(), size=100,)

class Panipat_Sheet(models.Model):
	date = models.DateField(default=date.today(), editable=False, primary_key=True, input_formats=["%d-%m-%Y"])
	generation = models.PositiveIntegerField()
	performance_ratio = models.PercentageField(verbose_name='Performance Ratio(PR)')
	irradiance = models.DecimalField(max_places=5, decimal_places=2, verbose_name='Irradiance(Inclined)')
	irradiance_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Low Irradiance')
	deemed_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Deemed')
	grid_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss sue to GRID outage')
	bd_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to BD')
	dust_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Dust')
	misc_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Misc. Losses')
	major_observations = models.ListTextField(
		observation=CharField(), size=100,)

class Roorkee_Sheet(models.Model):
	date = models.DateField(default=date.today(), editable=False, primary_key=True, input_formats=["%d-%m-%Y"])
	generation = models.PositiveIntegerField()
	performance_ratio = models.PercentageField(verbose_name='Performance Ratio(PR)')
	irradiance = models.DecimalField(max_places=5, decimal_places=2, verbose_name='Irradiance(Inclined)')
	irradiance_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Low Irradiance')
	deemed_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Deemed')
	grid_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss sue to GRID outage')
	bd_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to BD')
	dust_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Dust')
	misc_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Misc. Losses')
	major_observations = models.ListTextField(
		observation=CharField(), size=100,)

class Jharkhand_Sheet(models.Model):
	date = models.DateField(default=date.today(), editable=False, primary_key=True, input_formats=["%d-%m-%Y"])
	generation = models.PositiveIntegerField()
	performance_ratio = models.PercentageField(verbose_name='Performance Ratio(PR)')
	irradiance = models.DecimalField(max_places=5, decimal_places=2, verbose_name='Irradiance(Inclined)')
	irradiance_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Low Irradiance')
	deemed_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Deemed')
	grid_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss sue to GRID outage')
	bd_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to BD')
	dust_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Dust')
	misc_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Misc. Losses')
	major_observations = models.ListTextField(
		observation=CharField(), size=100,)

class Castamet_Sheet(models.Model):
	date = models.DateField(default=date.today(), editable=False, primary_key=True, input_formats=["%d-%m-%Y"])
	generation = models.PositiveIntegerField()
	performance_ratio = models.PercentageField(verbose_name='Performance Ratio(PR)')
	irradiance = models.DecimalField(max_places=5, decimal_places=2, verbose_name='Irradiance(Inclined)')
	irradiance_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Low Irradiance')
	deemed_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Deemed')
	grid_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss sue to GRID outage')
	bd_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to BD')
	dust_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Loss due to Dust')
	misc_loss = models.DecimalField(max_places=3, decimal_places=1, verbose_name='Misc. Losses')
	major_observations = models.ListTextField(
		observation=CharField(), size=100,)