from django.contrib import admin
from .models import Facturas, Clientes

# Register your models here.
admin.site.register(Facturas)
admin.site.register(Clientes)