# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Personalizamos el modelo User
class CustomUserAdmin(BaseUserAdmin):
	# Lista de campos que aparecerán en la vista de lista de usuarios
	list_display = (
		'username',
		'email',
		'first_name',
		'last_name',
		'is_staff',
		'is_active',
		'get_is_superuser',
		'get_groups'
	)

	def get_is_superuser(self, obj):
		if obj.is_superuser:
			return format_html("<img src='/static/admin/img/icon-yes.svg'")
		return format_html("<img src='/static/admin/img/icon-no.svg'")
	get_is_superuser.short_description = "S.U."
	get_is_superuser.admin_order_field = 'is_superuser'

	def get_groups(self, obj):
		group_html = ""
		for group in obj.groups.all().order_by('name'):
			# Asignamos una clase a cada grupo basado en el nombre del grupo
			title = "?"
			if group.name == 'UserManager':
				title = "Puede gestionar sus recursos de usuario (datos y perfil)"
			if group.name == 'RemoteConfig':
				title = "Puede usar las funciones remotas con el termostato"
			if group.name == 'UserAlarmManager':
				title = "Puede usar las funciones de alarmas"
			if group.name == 'UserTranslator':
				title = "Puede usar RosssetaTranslator"
			if group.name == 'UserHistoryDataExport':
				title = "Puede usar Exportador de InputHistory"
			if group.name == 'UserHistoryDataImport':
				title = "Puede usar Importador de InputHistory"
			if group_html:
				group_html += "<br>"
			group_html += format_html(
				'<span title="{}" class="group-admin-list group-{}" style="padding: 5px 10px; margin-right: 5px; border-radius: 5px; display: inline-block;">{}</span>',
				title,
				group.name,
				group.name
			)
		return format_html(group_html)
	get_groups.short_description = 'Grupos'


# Registramos la personalización del User Admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
