# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class GraphicHistorySettings(models.Model):

	"""
		Este modelo recoge los valores enviados por el termostato como valores historicos
	"""

	class Meta:
		verbose_name = _("Configuración Gráfico de dato histórico")
		verbose_name_plural = _("Configuración Gráficos de datos históricos")

	def __str__(self):
		return _("Configuración Gráficos de dato histórico ID [{id}] del usuario [{user}]").format(
			id=self.pk,
			user=self.user_id.username
		)

	TYPE_CHOICES = [
		('line', _('Lineas rectas')),
		('spline', _('Lineas curvadas')),
		('column', _('Columnas')),
		('widebars', 'Barras anchas')
	]

	LEGEND_POSITION = [
		('horizontal', _('Horizontal')),
		('vertical', _('Vertical')),
	]

	LEGEND_HORIZONTAL_ALIGN = [
		('left', _('Izquierda')),
		('center', _('Centro')),
		('right', _('Derecha')),
	]
	LEGEND_VERTICAL_ALIGN = [
		('top', _('Arriba')),
		('middle', _('Medio')),
		('bottom', _('Abajo')),
	]

	user_id = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Creación"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización"))

	legend_enable = models.BooleanField(blank = False, null = False, default = True)
	legend_position = models.CharField(max_length=10, default = "horizontal", choices = LEGEND_POSITION)
	legend_horizontal_align = models.CharField(max_length=10, default = "center", choices = LEGEND_HORIZONTAL_ALIGN)
	legend_vertical_align = models.CharField(max_length=10, default = "top", choices = LEGEND_VERTICAL_ALIGN)

	temps_scale_min = models.IntegerField(blank = False, null = False, default = 0)
	temps_scale_max = models.IntegerField(blank = False, null = False, default = 0)

	booleans_scale_min = models.IntegerField(blank = False, null = False, default = 0)
	booleans_scale_max = models.IntegerField(blank = False, null = False, default = 12)

	data_temp_visible = models.BooleanField(blank = True, null = True, default = True)
	data_temp_type = models.CharField(max_length=20, default = "spline", choices = TYPE_CHOICES)
	data_temp_fill = models.BooleanField(blank = True, null = True, default = False)
	data_temp_opacity = models.IntegerField(blank = True, null = True, default = 100)
	data_temp_color = models.CharField(max_length = 7, default = "#FF0000")
	data_temp_points = models.BooleanField(blank = True, null = True, default = False)

	data_hum_visible = models.BooleanField(blank = True, null = True, default = True)
	data_hum_type = models.CharField(max_length=20, default = "spline", choices = TYPE_CHOICES)
	data_hum_fill = models.BooleanField(blank = True, null = True, default = False)
	data_hum_opacity = models.IntegerField(blank = True, null = True, default = 100)
	data_hum_color = models.CharField(max_length = 7, default = "#FF0000")
	data_hum_points = models.BooleanField(blank = True, null = True, default = False)
