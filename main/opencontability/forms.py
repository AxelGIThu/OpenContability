from django import forms
from . import models

class CrearCliente(forms.ModelForm):
    class Meta:
        model = models.Clientes
        fields = ['nombre', 'CUIT', 'IVA']

class CrearFactura(forms.ModelForm):
    class Meta:
        model = models.Facturas
        fields = ['NFactura', 'Compra_o_Venta', 'Comprobante', 'Procesamiento', 'TComprobante', 'NComprobante', 'Movimiento', 'TImputacion', 'CUIT', 'Cliente', 'Comerciante', 'Importe']