# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InputDataHistoryConfig(AppConfig):

	name = 'apps.input_data_history'
	verbose_name = _('Datos de Entrada - Historial')
