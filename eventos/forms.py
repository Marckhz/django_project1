from django import forms
from .models import Evento
import datetime


class CrearEventoForm(forms.ModelForm):

	title = forms.CharField(label = 'Titulo', required=True)
	description = forms.CharField(label='Descripcion', required=True, widget=forms.Textarea)
	dead_line = forms.DateField(label='fecha', required=True, initial=datetime.date.today,widget=forms.SelectDateWidget)

	class Meta:
		model = Evento
		fields = ('title', 'description', 'dead_line')


	
