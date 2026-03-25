from django import forms
from .models import *

class BaseForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['aprovado', 'criado_por']


class PontoTuristicoForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = PontoTuristico


class HotelForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Hotel


class RestauranteForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Restaurante


class EventoForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Evento