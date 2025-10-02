from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from . import choices
from django.utils import timezone

class CrearCliente(forms.ModelForm):
    class Meta:
        model = models.Clientes
        fields = ['nombre', 'CUIT', 'IVA']

class CrearFactura(forms.ModelForm):
    NFactura = forms.CharField(label='Numero de Factura')
    Comprobante = forms.DateField(label='Fecha del Comprobante', widget=forms.DateInput(attrs={'type': 'date'}))
    TComprobante = forms.ChoiceField(choices=choices.choices_TComprobante)
    TImputacion = forms.ChoiceField(choices=choices.choices_TImputacion)
    Neto10y5 = forms.DecimalField(label='Neto 10,5%', max_digits=12, decimal_places=2, initial=0)
    IVA10y5 = forms.DecimalField(label='IVA 10,5%', max_digits=12, decimal_places=2, initial=0)
    Neto21 = forms.DecimalField(label='Neto 21%', max_digits=12, decimal_places=2, initial=0)
    IVA21 = forms.DecimalField(label='IVA 21%', max_digits=12, decimal_places=2, initial=0)
    Neto27 = forms.DecimalField(label='Neto 27%', max_digits=12, decimal_places=2, initial=0)
    IVA27 = forms.DecimalField(label='IVA 27%', max_digits=12, decimal_places=2, initial=0)
    ConceptoNoAgrabado = forms.DecimalField(label='Concepto No Gravado', max_digits=12, decimal_places=2, initial=0)
    PercepcionIVA = forms.DecimalField(label='Percepción IVA', max_digits=12, decimal_places=2, initial=0)
    PercepcionDGR = forms.DecimalField(label='Percepción DGR', max_digits=12, decimal_places=2, initial=0)
    PercepcionMunicipalidad = forms.DecimalField(label='Percepción Municipalidad', max_digits=12, decimal_places=2, initial=0)
    Otros = forms.DecimalField(label='Otros', max_digits=12, decimal_places=2, initial=0)
    Total = forms.DecimalField(label='Total', max_digits=12, decimal_places=2, initial=0)

    class Meta:
        model = models.Facturas
        fields = ['NFactura', 'Movimiento', 'Empresa', 'Cliente', 'Comprobante', 'TComprobante', 'TImputacion','Neto10y5', 'IVA10y5', 'Neto21', 'IVA21', 'Neto27', 'IVA27', 'ConceptoNoAgrabado', 'PercepcionIVA', 'PercepcionDGR', 'PercepcionMunicipalidad', 'Otros', 'Total']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
        # Filtramos las opciones de Cliente y Comerciante por el usuario actual
        self.fields['Empresa'].queryset = models.Clientes.objects.filter(propietario=user)
        self.fields['Cliente'].queryset = models.Clientes.objects.filter(propietario=user)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Introduce una dirección válida.')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está en uso.")
        return email