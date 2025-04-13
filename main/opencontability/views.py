from django.http import HttpResponse
from django.shortcuts import render
from .forms import CrearCliente

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
    return render(request, "tabla_clientes.html")

def cargar_facturas(request):
    return render(request, "cargar_facturas.html")

def tabla_compra_venta(request):
    return render(request, "tabla_compra_venta.html")

def modificar(request):
    return render(request, "modificar.html")

def generar_archivos(request):
    return render(request, "generar_archivos.html")