# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.db import models
from django.utils import timezone

from apps.common_functions import get_dev_num_str

class InputDataHistory(models.Model):

	"""
		Este modelo recoge los valores enviados por el termostato como valores historicos
	"""

	class Meta:
		verbose_name = "Historial de Datos de Entrada de Termostato"
		verbose_name_plural = "Historiales de Datos de Entradas de Termostatos"
		constraints = [
			models.UniqueConstraint(fields=['data_dev_num', 'created_at'], name='unique_user_created_at')
		]

	def __str__(self):
		return "Dato historico ID [{id}] del sensor [{data_dev_num_str}]".format(
			id=self.pk,
			data_dev_num_str=get_dev_num_str(self.data_dev_num)
		)

	created_at = models.DateTimeField(blank = True, null = True)
	data_dev_num = models.IntegerField(blank = True, null = True)
	data_temp = models.FloatField(blank = True, null = True)
	data_hum = models.FloatField(blank = True, null = True)

	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = timezone.now()
		super().save(*args, **kwargs)
