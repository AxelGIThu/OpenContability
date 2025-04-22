from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CrearCliente, CrearFactura
from .models import Clientes, Facturas
from django.db.models import Q

# Muestra los hipervinculos para las partes de la página.
# Tendrá verificación de usuarios en un futuro
def index(request):
    return render(request, "index.html")

# Cargar los clientes.
def nuevo_clientes(request):

    if request.method == "POST":
        # Crea un objeto con los datos del formulario y lo guarda.
        form = CrearCliente(request.POST)
        form.save()
        return HttpResponse("Funciono!<br><a href='nuevo_clientes'>Volver</a>")
    
    else:
        # Crea un objeto con el formulario para el HTML.
        form = CrearCliente

    return render(request, "nuevo_clientes.html", { 'form' : form})

def tabla_clientes(request):

    clientes = Clientes.objects.all()

    return render(request, "tabla_clientes.html", { 'clientes' : clientes})

def cargar_facturas(request):

    if request.method == "POST":
        # Crea un objeto con los datos del formulario y lo guarda.
        form = CrearFactura(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.calcular_totales()
            factura.save()
            return HttpResponse("Funciono!<br><a href='cargar_facturas'>Volver</a>")
    
    else:
        # Crea un objeto con el formulario para el HTML.
        form = CrearFactura

    return render(request, "cargar_facturas.html", { 'form' : form })

def tabla_compra_venta(request):

    if request.method == 'POST':

        if 'filtro_campos' in request.POST:
            # Si se seleccionaron columnas, crea una lista con los compos.
            columnas = request.POST.getlist('filtro_campos')
            facturas = Facturas.objects.all()

            if facturas:
                # Si hay facturas, las muestra
                return render(request, "tabla_compra_venta.html", { 'facturas' : facturas , 'columnas' : columnas })
            else:
                # Si no hay facturas, no las muestra.
                return render(request, "tabla_compra_venta.html")
            
    return render(request, "tabla_compra_venta.html")

def modificar_clientes(request, primary_key):
    cliente = get_object_or_404(Clientes, IDCliente=primary_key)
    form = CrearCliente(instance=cliente)
    
    if request.method == 'POST':

        form = CrearCliente(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('tabla_clientes')
    return render(request, "modificar_clientes.html", { 'form' : form, 'cliente' : cliente})

def modificar_facturas(request):
    
    return render(request, "modificar_facturas.html")

def generar_archivos(request):
    return render(request, "generar_archivos.html")