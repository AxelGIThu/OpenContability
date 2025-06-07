from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CrearCliente(forms.ModelForm):
    class Meta:
        model = models.Clientes
        fields = ['nombre', 'CUIT', 'IVA']

class CrearFactura(forms.ModelForm):
    class Meta:
        model = models.Facturas
        fields = ['NFactura', 'Compra_o_Venta', 'Comprobante', 'Procesamiento', 'TComprobante', 'NComprobante', 'Movimiento', 'TImputacion', 'Cliente', 'Comerciante', 'Importe']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Introduce una dirección válida.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está en uso.")
        return email