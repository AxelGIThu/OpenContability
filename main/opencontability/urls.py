from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Usuarios
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),

    # Verificación Email
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    
    ##########

    # Index
    path("", views.index, name="index"),
    ##########

    # Clientes
    path("clientes", views.index_clientes, name="clientes"),
    path("clientes/cargar_clientes", views.cargar_clientes, name="cargar_clientes"),
    path("clientes/tabla_clientes", views.tabla_clientes, name="tabla_clientes"),
    path("clientes/tabla_clientes/modificar_clientes/<int:primary_key>", views.modificar_clientes, name="modificar_clientes"),

    # Facturas
    path("facturas", views.index_facturas, name="facturas"),
    path("facturas/cargar_factura", views.cargar_facturas, name="cargar_facturas"),
    path("facturas/tabla_facturas", views.tabla_facturas, name="tabla_facturas"),
    path("facturas/tabla_facturas/modificar_facturas/<int:primary_key>", views.modificar_facturas, name="modificar_facturas"),
    ###########

    # Generar Archivos
    path("generar_archivos", views.generar_archivos, name="generar_archivos"),
    ###########
]