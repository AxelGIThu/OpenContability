from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("nuevo_clientes", views.nuevo_clientes, name="nuevo_clientes"),
    path("tabla_clientes", views.tabla_clientes, name="tabla_clientes"),
    path("cargar_facturas", views.cargar_facturas, name="cargar_factura"),
    path("tabla_compra_venta", views.tabla_compra_venta, name="tabla_compra_venta"),
    path("modificar", views.modificar, name="modificar"),
    path("generar_archivos", views.generar_archivos, name="generar_archivos"),
]