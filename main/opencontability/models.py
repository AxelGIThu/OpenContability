from django.db import models
from decimal import Decimal

# Create your models here.
class Clientes(models.Model):
    IDCliente = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    CUIT = models.CharField(max_length=11)
    IVA = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'Clientes'

class Facturas(models.Model):
    NFactura = models.IntegerField(primary_key=True)
    Compra_o_Venta = models.CharField(max_length=50)
    Comprobante = models.DateField()
    Procesamiento = models.DateField()
    TComprobante = models.CharField(max_length=100)
    NComprobante = models.CharField(max_length=100)
    Movimiento = models.CharField(max_length=100)
    TImputacion = models.CharField(max_length=100)
    CUIT = models.CharField(max_length=11)
    Cliente = models.CharField(max_length=150)
    Comerciante = models.CharField(max_length=150)

    Importe = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
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

    class Meta:
        db_table = 'Facturas'

    def save(self, *args, **kwargs):
        # Convertir campos None a Decimal(0)
        def safe_decimal(value):
            return value if value is not None else Decimal(0)

        # Calcular el total a partir de los demás campos
        total = (
            safe_decimal(self.Neto10y5) + safe_decimal(self.IVA10y5) +
            safe_decimal(self.Neto21) + safe_decimal(self.IVA21) +
            safe_decimal(self.Neto27) + safe_decimal(self.IVA27) +
            safe_decimal(self.ConceptoNoAgrabado) + safe_decimal(self.PercepcionIVA) +
            safe_decimal(self.PercepcionDGR) + safe_decimal(self.PercepcionMunicipalidad) +
            safe_decimal(self.Otros)
        )

        self.Total = total
        super().save(*args, **kwargs)