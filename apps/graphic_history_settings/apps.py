# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GraphicHistorySettingsConfig(AppConfig):

	name = 'apps.graphic_history_settings'
	verbose_name = _('Configuración Gráficos datos históricos')
