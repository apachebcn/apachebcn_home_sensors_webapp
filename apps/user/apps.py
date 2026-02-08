# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.utils.translation import gettext_lazy as _

from django.apps import AppConfig


class UserProfileConfig(AppConfig):

	name = 'apps.user'

	verbose_name = _('User')

