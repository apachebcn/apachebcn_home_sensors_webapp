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
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Creación"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización"))
	times_repeated_answer = models.IntegerField(blank = False, null = False, default = 0)

	data_s1_temp = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s1_temp_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s1_temp_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s1_hum = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s1_hum_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s1_hum_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s1_updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización S1"))

	# habitación matrimonio
	data_s2_temp = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s2_temp_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s2_temp_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s2_hum = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s2_hum_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s2_hum_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s2_updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización S2"))

	# habitación oficina
	data_s3_temp = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s3_temp_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s3_temp_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s3_hum = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s3_hum_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s3_hum_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s3_updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización S3"))

	# habitación wc arriba
	data_s4_temp = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s4_temp_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s4_temp_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s4_hum = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s4_hum_min = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s4_hum_max = models.CharField(max_length = 10, default = None, null = True, blank=True)
	data_s4_updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización S4"))

	data_from_thermostate_local_ip = models.CharField(max_length = 30, default = None, null = True, blank=True)
	data_from_thermostate_public_ip = models.CharField(max_length = 30, default = None, null = True, blank=True)
