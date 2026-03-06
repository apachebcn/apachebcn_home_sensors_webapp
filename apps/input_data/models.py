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
		return _("Dato ID [{id}] del sensor [{room_id_str}]").format(
			id=self.pk,
			room_id_str=get_dev_num_str(self.room_id)
		)

	RELAY_CHOICES = [
		('0', 'Automático'),
		('1', 'Forzado ON'),
		('2', 'Forzado OFF')
	]

	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización"))
	times_repeated_answer = models.IntegerField(blank = False, null = False, default = 0)

	room_id = models.IntegerField(null=False, blank=False, unique=True)
	room_data_temp = models.FloatField(null = False, blank=False)
	room_data_temp_min = models.FloatField(default = None, null = True, blank=True)
	room_data_temp_max = models.FloatField(default = None, null = True, blank=True)
	room_data_hum = models.FloatField(null = False, blank=False)
	room_data_hum_min = models.FloatField(default = None, null = True, blank=True)
	room_data_hum_max = models.FloatField(default = None, null = True, blank=True)
	room_version = models.CharField(max_length=20, default=None, null=True, blank=True)
	room_mark_to_update = models.BooleanField(default=False, blank=False, null=False)
