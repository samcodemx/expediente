from django import forms
from .models import Medico, Valoracion
from django.contrib.auth.forms import AuthenticationForm


class Medico_form(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ()


class Valoracion_form(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ()

class Login_form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))