# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class InputDataHistory(models.Model):

	"""
		Este modelo recoge los valores enviados por el termostato como valores historicos
	"""

	class Meta:
		verbose_name = _("Historial de Datos de Entrada de Termostato")
		verbose_name_plural = _("Historiales de Datos de Entradas de Termostatos")
		constraints = [
			models.UniqueConstraint(fields=['user_id', 'created_at'], name='unique_user_created_at')
		]

	def __str__(self):
		return _("Dato historico del termostato ID [{id}] del usuario [{user}]").format(
			id=self.pk,
			user=self.user_id.username
		)

	user_id = models.ForeignKey(User, on_delete = models.CASCADE)
	created_at = models.DateTimeField(blank = True, null = True)
	data_s1_temp = models.FloatField(blank = True, null = True)
	data_s1_hum = models.FloatField(blank = True, null = True)
	data_s2_temp = models.FloatField(blank = True, null = True)
	data_s2_hum = models.FloatField(blank = True, null = True)
	data_s3_temp = models.FloatField(blank = True, null = True)
	data_s3_hum = models.FloatField(blank = True, null = True)
	data_s4_temp = models.FloatField(blank = True, null = True)
	data_s4_hum = models.FloatField(blank = True, null = True)

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()
		super().save(*args, **kwargs)
