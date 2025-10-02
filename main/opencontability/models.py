from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

# Create your models here.
class Clientes(models.Model):
    IVA_CHOICES = [
        ('Inscripto','Inscripto'),
        ('No inscripto','No Inscripto')
    ]

    IDCliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    CUIT = models.CharField(max_length=11)
    IVA = models.CharField(max_length=20, choices=IVA_CHOICES)

    # Usuario propietario.
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Clientes'
    
    def __str__(self):
        return f'{self.nombre}'

class Facturas(models.Model):
    COMPRA_O_VENTA_CHOICES = [
        ('compra','Compra'),
        ('venta','Venta')
    ]

    NFactura = models.CharField(primary_key=True)
    Movimiento = models.CharField(max_length=6, choices=COMPRA_O_VENTA_CHOICES)
    Comprobante = models.DateField()
    Procesamiento = models.DateField(auto_now_add=True)
    TComprobante = models.CharField(max_length=100)
    # NComprobante = models.CharField(max_length=100)
    TImputacion = models.CharField(max_length=100)
    # TLiquidacion = models.CharField(max_length=100)
    
    Empresa = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    Cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name="+")

    # Importe = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    Neto10y5 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    IVA10y5 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    Neto21 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    IVA21 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    Neto27 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    IVA27 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ConceptoNoAgrabado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PercepcionIVA = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PercepcionDGR = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PercepcionMunicipalidad = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    Otros = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    Total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Usuario propietario.
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Facturas'