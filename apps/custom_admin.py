# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial

from django.contrib import admin

from apps.common_functions import get_realuser_is_superuser

import logging
logger = logging.getLogger('django')

from django.contrib.admin import ModelAdmin


def admin_get_queryset(admin_instance, request):
	"""
	Devuelve el queryset filtrado por usuario si no es un superusuario.
	"""
	# Obtiene el queryset usando ModelAdmin directamente
	qs = ModelAdmin.get_queryset(admin_instance, request)
	if get_realuser_is_superuser(request):
		return qs

	model_name = admin_instance.model.__name__
	# logger.info(f"El nombre del modelo es: {model_name}")

	if model_name == "UserAlarmLog":
		return qs.filter(useralarm_id__user_id=request.user.id)

	return qs.filter(user_id=request.user.id)


def admin_save_user_model(request, obj, form, change):
	"""
	Asigna el usuario actual al campo user_id si es una nueva instancia.
	"""
	# if form.instance._meta.model_name == 'useralarm':
	if not obj.pk:
		obj.user_id = request.user  # Asignar el ID del usuario, no el objeto
	obj.save()
	return

	# if not obj.pk:
	# 	obj.user_id = request.user.id  # Asignar el ID del usuario, no el objeto
	# obj.save()


def admin_has_permission(request, model, codename, obj):
	"""
		Permisos aplicados a los users no admin
		No lo estoy usando porque parece estar funcionando automaticamente, pero lo tengo preparado por si acaso
	"""
	from django.contrib.auth.models import Permission
	from django.contrib.contenttypes.models import ContentType

	if get_realuser_is_superuser(request):
		return True

	if obj is not None and request.user != obj.user_id:
		return False

	# Obtener el content type para el modelo dado
	content_type = ContentType.objects.get_for_model(model)

	# Construir el codename completo
	full_codename = f"{content_type.app_label}.{codename}"

	# Verificar si el permiso existe
	try:
		permission = Permission.objects.get(
			codename=codename,
			content_type=content_type,
		)
	except Permission.DoesNotExist:
		logger.error(f"El permiso {full_codename} no existe para el modelo {model}.")
		return False

	# Verificar si el usuario tiene el permiso
	if request.user.has_perm(full_codename):
		return True
	else:
		return False


class CustomAdmin(admin.ModelAdmin):

	class Media:
		js = '/static/project/admin_override/js/admin_models_hide_menu.js',

	def get_queryset(self, request):
		return admin_get_queryset(self, request)

	def save_model(self, request, obj, form, change):
		admin_save_user_model(request, obj, form, change)

	def get_form(self, request, obj=None, **kwargs):
		"""
		Devuelve el formulario personalizado para el administrador.
		Si el usuario no es un superusuario, excluye el campo 'user_id'.
		"""
		form = super().get_form(request, obj, **kwargs)
		if not get_realuser_is_superuser(request):
			form.base_fields.pop('user_id', None)  # Excluir el campo user_id
		form.user = request.user  # Pasar el usuario actual al formulario
		return form

	def get_fieldsets(self, request, obj=None):
		"""
		Devuelve los fieldsets para el formulario del admin.
		Excluye 'user_id' si el usuario no es un superusuario.
		"""
		# logger.info("get_fieldsets called")  # Depuración
		fieldsets = super().get_fieldsets(request, obj)
		if get_realuser_is_superuser(request):
			return fieldsets
		new_fieldsets = []
		for title, options in fieldsets:
			fields = tuple(
				field for field in options.get('fields', [])
				if field != 'user_id'
			)
			new_fieldsets.append((title, {'fields': fields}))
		return new_fieldsets

	def remove_fields_of_fieldsets_for_users(self, request, fieldsets, fieldnames):
		"""
		Excluye una lista de campos específicos de los fieldsets si el usuario no es superusuario.

		Args:
			request (HttpRequest): La solicitud que contiene la información del usuario.
			fieldsets (list of tuples): Lista de fieldsets a modificar.
			fieldnames (list of str): Lista de nombres de campos a eliminar de los fieldsets.

		Returns:
			list of tuples: Lista de fieldsets con los campos especificados excluidos si el usuario no es superusuario.
		"""
		if get_realuser_is_superuser(request):
			return fieldsets
		# Filtrar los campos específicos de cada fieldset
		new_fieldsets = []
		for title, options in fieldsets:
			fields = tuple(
				field for field in options.get('fields', [])
				if field not in fieldnames
			)
			new_fieldsets.append((title, {'fields': fields}))
		return new_fieldsets
