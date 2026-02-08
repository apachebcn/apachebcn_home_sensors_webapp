# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common_functions import get_dev_num_str


class InputData(models.Model):

	"""
		Este modelo recoge los valores enviados por el termostato
		Representa los ultimos valores recibidos para representarlo en un panel informativo
	"""

	class Meta:
		verbose_name = "Dato de entrada"
		verbose_name_plural = "Datos de entrada"

	def __str__(self):
		return _("Dato ID [{id}] del sensor [{data_dev_num_str}]").format(
			id=self.pk,
			data_dev_num_str=get_dev_num_str(self.data_dev_num)
		)

	RELAY_CHOICES = [
		('0', 'Automático'),
		('1', 'Forzado ON'),
		('2', 'Forzado OFF')
	]

	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización"))
	times_repeated_answer = models.IntegerField(blank = False, null = False, default = 0)

	data_dev_num = models.IntegerField(null=False, blank=False, unique=True)
	data_temp = models.FloatField(null = False, blank=False)
	data_temp_min = models.FloatField(default = 0, null = True, blank=True)
	data_temp_max = models.FloatField(default = 0, null = True, blank=True)
	data_hum = models.FloatField(null = False, blank=False)
	data_hum_min = models.FloatField(default = 0, null = True, blank=True)
	data_hum_max = models.FloatField(default = 0, null = True, blank=True)

	data_from_thermostate_local_ip = models.CharField(max_length = 30, default = None, null = True, blank=True)
	data_from_thermostate_public_ip = models.CharField(max_length = 30, default = None, null = True, blank=True)
