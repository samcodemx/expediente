from django import forms
from .models import Medico, Valoracion

class Medico_form(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ()
