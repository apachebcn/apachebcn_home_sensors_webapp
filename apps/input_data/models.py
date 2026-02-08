# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class InputData(models.Model):

	"""
		Este modelo recoge los valores enviados por el termostato
		Representa los ultimos valores recibidos para representarlo en un panel informativo
	"""

	class Meta:
		verbose_name = _("Dato de entrada")
		verbose_name_plural = _("Datos de entrada")

	def __str__(self):
		return _("Dato de entrada del termostato ID [{id}] del usuario [{user}]").format(
			id=self.pk,
			user=self.user_id.username
		)

	RELAY_CHOICES = [
		('0', _('Automático')),
		('1', _('Forzado ON')),
		('2', _('Forzado OFF'))
	]

	user_id = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización"))
	times_repeated_answer = models.IntegerField(blank = False, null = False, default = 0)

	data_dev_num = models.IntegerField(null = False, blank=False)
	data_temp = models.FloatField(null = False, blank=False)
	data_temp_min = models.FloatField(default = 0, null = True, blank=True)
	data_temp_max = models.FloatField(default = 0, null = True, blank=True)
	data_hum = models.FloatField(null = False, blank=False)
	data_hum_min = models.FloatField(default = 0, null = True, blank=True)
	data_hum_max = models.FloatField(default = 0, null = True, blank=True)

	data_from_thermostate_local_ip = models.CharField(max_length = 30, default = None, null = True, blank=True)
	data_from_thermostate_public_ip = models.CharField(max_length = 30, default = None, null = True, blank=True)
