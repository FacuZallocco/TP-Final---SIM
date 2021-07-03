from django import forms
from crispy_forms.helper import FormHelper

class ParametersForm(forms.Form):
    dias = forms.IntegerField(label='Dias a simular', initial=1000, min_value=0)
    diaInicio = forms.IntegerField(label='Dia inicio informe', initial=100, min_value=0)
    diaFin = forms.IntegerField(label='Dia fin informe', initial=200, min_value=0)
    limiteReposicion = forms.IntegerField(label='Limite de Reposicion', initial=540, min_value=0)
    cantReposicion = forms.IntegerField(label='Cantidad a reponer', initial=780, min_value=0)
    stock = forms.IntegerField(label='Stock Actual', initial=700, min_value=0)

    ko = forms.IntegerField(label='Costo de ordenar a la fábrica (Ko)', initial=50000, min_value=0)
    km = forms.IntegerField(label='Costo de llevar inventario (Km)', initial=350, min_value=0)
    ks = forms.IntegerField(label='Costo de faltante (Ks)', initial=9500, min_value=0)
    ki = forms.IntegerField(label='Costo de imagen (Ki)', initial=2000, min_value=0)
    kc = forms.IntegerField(label='Costo de sobrepasar la capacidad del almacén (Kc)', initial=8000, min_value=0)
    aumento_demanda = forms.BooleanField(label='¿Desea aumentar la demanda en un 20%?', initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False
