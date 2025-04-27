from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
import xlsxwriter.worksheet
from .forms import CrearCliente, CrearFactura
from .models import Clientes, Facturas
from django.db.models import Q
import xlsxwriter

# Muestra los hipervinculos para las partes de la página.
# Tendrá verificación de usuarios en un futuro
def index(request):
    return render(request, "index.html")

########################################################## Clientes
def index_clientes(request):
    return render(request, "clientes.html")

def cargar_clientes(request):

    if request.method == "POST":
        # Crea un objeto con los datos del formulario y lo guarda.
        form = CrearCliente(request.POST)
        form.save()
        return HttpResponse("Funciono!<br><a class='anchor' href='cargar_clientes'>Volver</a>")
    
    else:
        # Crea un objeto con el formulario para el HTML.
        form = CrearCliente()

    return render(request, "cargar_clientes.html", { 'form' : form})

def tabla_clientes(request):

    clientes = Clientes.objects.all()

    return render(request, "tabla_clientes.html", { 'clientes' : clientes})

##########################################################

########################################################## Facturas
def index_facturas(request):
    return render(request, "facturas.html")

def cargar_facturas(request):

    if request.method == "POST":
        # Crea un objeto con los datos del formulario y lo guarda.
        form = CrearFactura(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.calcular_totales()
            factura.save()
            return HttpResponse("Funciono!<br><a class='anchor' href='..'>Volver</a>")
    
    else:
        # Crea un objeto con el formulario para el HTML.
        form = CrearFactura()

    return render(request, "cargar_facturas.html", { 'form' : form })

def tabla_facturas(request):

    if request.method == 'POST':

        if 'filtro_campos' in request.POST:
            # Si se seleccionaron columnas, crea una lista con los compos.
            columnas = request.POST.getlist('filtro_campos')
            facturas = Facturas.objects.all()

            if facturas:
                # Si hay facturas, las muestra
                return render(request, "tabla_facturas.html", { 'facturas' : facturas , 'columnas' : columnas })
            else:
                # Si no hay facturas, no las muestra.
                return render(request, "tabla_facturas.html")
            
    return render(request, "tabla_facturas.html")

##########################################################

########################################################## Modificar
def modificar_clientes(request, primary_key):
    cliente = get_object_or_404(Clientes, IDCliente=primary_key)
    form = CrearCliente(instance=cliente)
    
    if request.method == 'POST':

        form = CrearCliente(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('tabla_clientes')
    return render(request, "modificar_clientes.html", { 'form' : form, 'cliente' : cliente})

def modificar_facturas(request, primary_key):
    factura = get_object_or_404(Facturas, NFactura=primary_key)
    form = CrearFactura(instance=factura)
    
    if request.method == 'POST':

        form = CrearFactura(request.POST, instance=factura)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.calcular_totales()
            factura.save()
            return redirect('tabla_facturas')
    return render(request, "modificar_facturas.html", { 'form' : form, 'factura' : factura})

##########################################################

########################################################## Generar Archivos
def generar_archivos(request):

    if request.POST:
        
        inicio = request.POST['inicio']
        final = request.POST['final']
        tipo = request.POST['tipo']
        nombre = request.POST['nombre']
        
        datos = get_list_or_404(Facturas, Comprobante__range=[inicio, final])

        if tipo == 'libro':
            libro = xlsxwriter.Workbook(f'{nombre}.xlsx')
            hoja = libro.add_worksheet('Libro')

            # Encabezado
            columnas = ['NumFactura', '¿Compra o Venta?', 'Comprobante', 'Procesamiento', 'Tipo de Comprobante', 'NumComprobante', 'Movimiento', 'Tipo de Imputación', 'CUIT', 'Cliente', 'Comerciante', 'Importe', 'Neto10y5', 'IVA10y5', 'Neto21', 'IVA21', 'Neto27', 'IVA27', 'ConceptoNoAgrabado', 'PercepcionIVA', 'PercepcionDGR', 'PercepcionMunicipalidad', 'Otros', 'Total']
            contador_columnas = 0
            for columna in columnas:
                hoja.write(0, contador_columnas, columna)
                contador_columnas+=1

            # Datos
            fila = 1
            for dato in datos:
                print(dato)
                hoja.write(fila, 0, dato.NFactura)
                hoja.write(fila, 1, dato.Compra_o_Venta)
                hoja.write(fila, 2, dato.Comprobante)
                hoja.write(fila, 3, dato.Procesamiento)
                hoja.write(fila, 4, dato.TComprobante)
                hoja.write(fila, 5, dato.NComprobante)
                hoja.write(fila, 6, dato.Movimiento)
                hoja.write(fila, 7, dato.TImputacion)
                hoja.write(fila, 8, dato.CUIT)
                hoja.write(fila, 9, dato.Cliente)
                hoja.write(fila, 10, dato.Comerciante)
                hoja.write(fila, 11, dato.Importe)
                hoja.write(fila, 12, dato.Neto10y5)
                hoja.write(fila, 13, dato.IVA10y5)
                hoja.write(fila, 14, dato.Neto21)
                hoja.write(fila, 15, dato.IVA21)
                hoja.write(fila, 16, dato.Neto27)
                hoja.write(fila, 17, dato.IVA27)
                hoja.write(fila, 18, dato.ConceptoNoAgrabado)
                hoja.write(fila, 19, dato.PercepcionIVA)
                hoja.write(fila, 20, dato.PercepcionDGR)
                hoja.write(fila, 21, dato.PercepcionMunicipalidad)
                hoja.write(fila, 22, dato.Otros)
                hoja.write(fila, 23, dato.Total)
                fila+=1
            
            hoja.write(fila+1, 10, 'Total')
            hoja.write(fila+1, 11, f'=SUM(L1:L{fila})')
            hoja.write(fila+1, 12, f'=SUM(M1:M{fila})')
            hoja.write(fila+1, 13, f'=SUM(N1:N{fila})')
            hoja.write(fila+1, 14, f'=SUM(O1:O{fila})')
            hoja.write(fila+1, 15, f'=SUM(P1:P{fila})')
            hoja.write(fila+1, 16, f'=SUM(Q1:Q{fila})')
            hoja.write(fila+1, 17, f'=SUM(R1:R{fila})')
            hoja.write(fila+1, 18, f'=SUM(S1:S{fila})')
            hoja.write(fila+1, 19, f'=SUM(T1:T{fila})')
            hoja.write(fila+1, 20, f'=SUM(U1:U{fila})')
            hoja.write(fila+1, 21, f'=SUM(V1:V{fila})')
            hoja.write(fila+1, 22, f'=SUM(W1:W{fila})')
            hoja.write(fila+1, 23, f'=SUM(X1:X{fila})')

            libro.close()


    return render(request, "generar_archivos.html")

##########################################################