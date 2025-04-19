from django.db import models
from decimal import Decimal

# Create your models here.
class Clientes(models.Model):
    IVA_CHOICES = [
        ('inscripto','Inscripto'),
        ('no_inscripto','No Inscripto')
    ]

    IDCliente = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    CUIT = models.CharField(max_length=11)
    IVA = models.CharField(max_length=20, choices=IVA_CHOICES)
    
    class Meta:
        db_table = 'Clientes'

class Facturas(models.Model):
    COMRPRA_O_VENTA_CHOICES = [
        ('compra','Compra'),
        ('venta','Venta')
    ]

    NFactura = models.IntegerField(primary_key=True)
    Compra_o_Venta = models.CharField(max_length=6, choices=COMRPRA_O_VENTA_CHOICES)
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
    
    def calcular_totales(self):
        from decimal import Decimal, ROUND_HALF_UP
    
        def safe_decimal(value):
            return value if value is not None else Decimal('0.00')
    
        importe_total = safe_decimal(self.Importe)
    
        iva_rate = Decimal('0.21')
        divisor = Decimal('1.21')
        neto = (importe_total / divisor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        iva = (importe_total - neto).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
        self.Neto21 = neto
        self.IVA21 = iva
    
        self.Neto10y5 = Decimal('0.00')
        self.IVA10y5 = Decimal('0.00')
        self.Neto27 = Decimal('0.00')
        self.IVA27 = Decimal('0.00')
        self.ConceptoNoAgrabado = Decimal('0.00')
        self.PercepcionIVA = Decimal('0.00')
        self.PercepcionDGR = Decimal('0.00')
        self.PercepcionMunicipalidad = Decimal('0.00')
        self.Otros = Decimal('0.00')
    
        self.Total = (
            self.Neto10y5 + self.IVA10y5 +
            self.Neto21 + self.IVA21 +
            self.Neto27 + self.IVA27 +
            self.ConceptoNoAgrabado + self.PercepcionIVA +
            self.PercepcionDGR + self.PercepcionMunicipalidad +
            self.Otros
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)