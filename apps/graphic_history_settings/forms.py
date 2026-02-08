# author PEDRO REINA ROJAS <apachebcn@gmail.com>
# copyright PEDRO REINA ROJAS (apachebcn@gmail.com)
# license comercial


from django import forms
from django.forms import ModelForm, CharField
from django.forms.widgets import TextInput
from .models import GraphicHistorySettings

import logging
logger = logging.getLogger('django')


class GraphicHistorySettingsForm(forms.ModelForm):
	class Meta:
		model = GraphicHistorySettings
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
				field.widget.attrs.update({'class': 'form-control custom-class'})
			elif isinstance(field.widget, forms.Select):
				field.widget.attrs.update({'class': 'form-control custom-class'})

			if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.Select, forms.CheckboxInput, forms.Textarea, forms.DateInput)):
				field.widget.attrs.update({
					# 'class': 'form-control custom-class',
					'id': f'id_{field_name}'
				})

			field.widget.attrs.update({
				'data-field': 'field-save',
			})

			color_fields = [
				"data_dev_num",
				"data_temp_color",
				"data_hum_color",
			]
			if field_name in color_fields:
				field.widget.input_type = 'color'

	def clean(self):
		cleaned_data = super().clean()
		# Aquí puedes agregar validaciones adicionales si es necesario
		return cleaned_data
