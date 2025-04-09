# Generated by Django 5.1.4 on 2025-04-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('IDCliente', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('CUIT', models.CharField(max_length=11)),
                ('IVA', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Facturas',
            fields=[
                ('NFactura', models.IntegerField(primary_key=True, serialize=False)),
                ('Compra_o_Venta', models.CharField(max_length=50)),
                ('Comprobante', models.DateField()),
                ('Procesamiento', models.DateField()),
                ('TComprobante', models.CharField(max_length=100)),
                ('NComprobante', models.CharField(max_length=100)),
                ('Movimiento', models.CharField(max_length=100)),
                ('TImputacion', models.CharField(max_length=100)),
                ('CUIT', models.CharField(max_length=11)),
                ('Cliente', models.CharField(max_length=150)),
                ('Comerciante', models.CharField(max_length=150)),
                ('Importe', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('Neto10y5', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('IVA10y5', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('Neto21', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('IVA21', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('Neto27', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('IVA27', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('ConceptoNoAgrabado', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('PercepcionIVA', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('PercepcionDGR', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('PercepcionMunicipalidad', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('Otros', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('Total', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'db_table': 'Facturas',
            },
        ),
    ]
