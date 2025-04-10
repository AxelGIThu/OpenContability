from django import forms
from . import models

class CrearCliente(forms.ModelForm):
    class Meta:
        model = models.Clientes
        fields = "__all__"