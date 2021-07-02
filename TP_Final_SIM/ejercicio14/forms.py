from django import forms
from crispy_forms.helper import FormHelper

class ParametersForm(forms.Form):
    dias = forms.IntegerField(label='Dias a simular',initial=1000,min_value=0)
    diaInicio = forms.IntegerField(label='Dia inicio informe',initial=0,min_value=0)
    diaFin = forms.IntegerField(label='Dia fin informe',initial=100,min_value=0)
    limiteReposicion = forms.IntegerField(label='Limite de Reposicion',initial=540,min_value=0)
    cantReposicion = forms.IntegerField(label='Cantidad a reponer',initial=780,min_value=0)
    stock = forms.IntegerField(label='Stock Actual',initial=700,min_value=0)
    capacidad = forms.IntegerField(label='Capacidad almacen', initial=1800, min_value=0)
    aumentoDemanda = forms.CheckboxInput(check_test=None)

    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False
