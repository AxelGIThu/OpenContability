from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from .forms import CrearCliente, CrearFactura, CustomUserCreationForm
from .models import Clientes, Facturas
import xlsxwriter, csv, io, os
from .funciones import is_valid_fecha, procesar_ocr_api, extraer_importe_total, extraer_fecha_emision, extraer_numero_factura, normalizar_importe
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Bloqueamos acceso hasta verificar
            user.save()

            # Generar token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construir URL de activación
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            # Enviar email
            subject = "Activa tu cuenta"
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, 'opencontability.noreply@gmail.com', [user.email])

            return HttpResponse('Revisa tu email para activar tu cuenta.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registro.html', {'form': form})

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Cuenta activada correctamente. Ya puedes iniciar sesión.")
    else:
        return HttpResponse("El link de activación no es válido o ha expirado.")

# Muestra los hipervinculos para las partes de la página.
# Tendrá verificación de usuarios en un futuro
@login_required
def index(request):
    return render(request, "index.html")

########################################################## Clientes
@login_required
def index_clientes(request):
    return render(request, "clientes.html")

@login_required
def cargar_clientes(request):

    if request.method == "POST":
        # Crea un objeto con los datos del formulario y lo guarda.
        form = CrearCliente(request.POST)
        if form.is_valid():
            varForm = form.save(commit=False)
            varForm.propietario = request.user
            varForm.save()
            form = CrearCliente()
            return render(request, "cargar_clientes.html", { 'form' : form })
    
    else:
        # Crea un objeto con el formulario para el HTML.
        form = CrearCliente()

    return render(request, "cargar_clientes.html", { 'form' : form })

@login_required
def tabla_clientes(request):

    clientes = Clientes.objects.filter(propietario=request.user)

    return render(request, "tabla_clientes.html", { 'clientes' : clientes })

##########################################################

########################################################## Facturas
@login_required
def index_facturas(request):
    return render(request, "facturas.html")

@login_required
def cargar_facturas(request):

    if request.method == "POST":
        # Crea un objeto con los datos del formulario y lo guarda.
        form = CrearFactura(request.POST, user=request.user)
        if form.is_valid():
            factura = form.save(commit=False)
            varFactura = factura
            varFactura.propietario = request.user
            varFactura.save()
            form = CrearFactura(user=request.user)
            return render(request, "cargar_facturas.html", { 'form' : form })
            form = CrearFactura(user=request.user)
            return render(request, "cargar_facturas.html", { 'form' : form })
    
    else:
        # Crea un objeto con el formulario para el HTML.
        form = CrearFactura(user=request.user)

    return render(request, "cargar_facturas.html", { 'form' : form })

@login_required
def tabla_facturas(request):

    if request.method == 'POST':

        if 'filtro_campos' in request.POST:
            # Si se seleccionaron columnas, crea una lista con los compos.
            columnas = request.POST.getlist('filtro_campos')
            facturas = Facturas.objects.filter(propietario=request.user)

            if facturas:
                # Si hay facturas, las muestra
                return render(request, "tabla_facturas.html", { 'facturas' : facturas , 'columnas' : columnas })
            else:
                # Si no hay facturas, no las muestra.
                return render(request, "tabla_facturas.html")
            
    return render(request, "tabla_facturas.html")

##########################################################

########################################################## Modificar
@login_required
def modificar_clientes(request, primary_key):
    cliente = get_object_or_404(Clientes, IDCliente=primary_key)
    form = CrearCliente(instance=cliente)
    
    if request.method == 'POST':

        form = CrearCliente(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('tabla_clientes')
    return render(request, "modificar_clientes.html", { 'form' : form, 'cliente' : cliente})

@login_required
def modificar_facturas(request, primary_key):
    factura = get_object_or_404(Facturas, NFactura=primary_key)
    form = CrearFactura(instance=factura, user=request.user.id)
    
    if request.method == 'POST':
        form = CrearFactura(request.POST, instance=factura, user=request.user.id)
        if form.is_valid():
            factura = form.save()
            factura = form.save()
            return redirect('tabla_facturas')
    return render(request, "modificar_facturas.html", { 'form' : form, 'factura' : factura})

##########################################################

########################################################## Generar Archivos
@login_required
def generar_archivos(request):

    if request.POST:
        inicio = request.POST['inicio']
        final = request.POST['final']

        if is_valid_fecha(inicio) and is_valid_fecha(final):

            tipo = request.POST['tipo']
            nombre = request.POST['nombre']

            datos = get_list_or_404(Facturas, Comprobante__range=[inicio, final])

            if tipo == 'libro':

                # Crea un buffer (El objeto que luego va a crear la señal para descargar el archivo)
                output = io.BytesIO()

                libro = xlsxwriter.Workbook(output, {'in_memory': True})
                hoja = libro.add_worksheet('Libro')
                date_format = libro.add_format({'num_format': 'dd/mm/yyyy'})
                date_format = libro.add_format({'num_format': 'dd/mm/yyyy'})

                # Encabezado
                columnas = ['Numero de Factura', 'Movimiento', 'Comprobante', 'Procesamiento', 'Tipo de Comprobante', 'Tipo de Imputación', 'Empresa', 'Cliente', 'Neto10y5', 'IVA10y5', 'Neto21', 'IVA21', 'Neto27', 'IVA27', 'ConceptoNoAgrabado', 'PercepcionIVA', 'PercepcionDGR', 'PercepcionMunicipalidad', 'Otros', 'Total']
                columnas = ['Numero de Factura', 'Movimiento', 'Comprobante', 'Procesamiento', 'Tipo de Comprobante', 'Tipo de Imputación', 'Empresa', 'Cliente', 'Neto10y5', 'IVA10y5', 'Neto21', 'IVA21', 'Neto27', 'IVA27', 'ConceptoNoAgrabado', 'PercepcionIVA', 'PercepcionDGR', 'PercepcionMunicipalidad', 'Otros', 'Total']
                contador_columnas = 0
                for columna in columnas:
                    hoja.write(0, contador_columnas, columna)
                    contador_columnas+=1

                # Datos
                fila = 1
                for dato in datos:
                    hoja.write(fila, 0, dato.NFactura)
                    hoja.write(fila, 1, dato.Movimiento)
                    hoja.write(fila, 2, dato.Comprobante, date_format)
                    hoja.write(fila, 3, dato.Procesamiento, date_format)
                    hoja.write(fila, 1, dato.Movimiento)
                    hoja.write(fila, 2, dato.Comprobante, date_format)
                    hoja.write(fila, 3, dato.Procesamiento, date_format)
                    hoja.write(fila, 4, dato.TComprobante)
                    hoja.write(fila, 5, dato.TImputacion)
                    hoja.write(fila, 6, dato.Empresa.CUIT)
                    hoja.write(fila, 7, dato.Cliente.CUIT)
                    hoja.write(fila, 8, dato.Neto10y5)
                    hoja.write(fila, 9, dato.IVA10y5)
                    hoja.write(fila, 10, dato.Neto21)
                    hoja.write(fila, 11, dato.IVA21)
                    hoja.write(fila, 12, dato.Neto27)
                    hoja.write(fila, 13, dato.IVA27)
                    hoja.write(fila, 14, dato.ConceptoNoAgrabado)
                    hoja.write(fila, 15, dato.PercepcionIVA)
                    hoja.write(fila, 16, dato.PercepcionDGR)
                    hoja.write(fila, 17, dato.PercepcionMunicipalidad)
                    hoja.write(fila, 18, dato.Otros)
                    hoja.write(fila, 19, dato.Total)
                    hoja.write(fila, 5, dato.TImputacion)
                    hoja.write(fila, 6, dato.Empresa.CUIT)
                    hoja.write(fila, 7, dato.Cliente.CUIT)
                    hoja.write(fila, 8, dato.Neto10y5)
                    hoja.write(fila, 9, dato.IVA10y5)
                    hoja.write(fila, 10, dato.Neto21)
                    hoja.write(fila, 11, dato.IVA21)
                    hoja.write(fila, 12, dato.Neto27)
                    hoja.write(fila, 13, dato.IVA27)
                    hoja.write(fila, 14, dato.ConceptoNoAgrabado)
                    hoja.write(fila, 15, dato.PercepcionIVA)
                    hoja.write(fila, 16, dato.PercepcionDGR)
                    hoja.write(fila, 17, dato.PercepcionMunicipalidad)
                    hoja.write(fila, 18, dato.Otros)
                    hoja.write(fila, 19, dato.Total)
                    fila+=1
                fila+=1
                hoja.write(fila, 7, 'Totales')
                hoja.write(fila, 8, f'=SUM(I2:I{fila})')
                hoja.write(fila, 9, f'=SUM(J2:J{fila})')
                hoja.write(fila, 7, 'Totales')
                hoja.write(fila, 8, f'=SUM(I2:I{fila})')
                hoja.write(fila, 9, f'=SUM(J2:J{fila})')
                hoja.write(fila, 10, f'=SUM(K2:K{fila})')
                hoja.write(fila, 11, f'=SUM(L2:L{fila})')
                hoja.write(fila, 12, f'=SUM(M2:M{fila})')
                hoja.write(fila, 13, f'=SUM(N2:N{fila})')
                hoja.write(fila, 14, f'=SUM(O2:O{fila})')
                hoja.write(fila, 15, f'=SUM(P2:P{fila})')
                hoja.write(fila, 16, f'=SUM(Q2:Q{fila})')
                hoja.write(fila, 17, f'=SUM(R2:R{fila})')
                hoja.write(fila, 18, f'=SUM(S2:S{fila})')
                hoja.write(fila, 19, f'=SUM(T2:T{fila})')

                libro.close()

                # Se da los valores al buffer para que este en el formato correcto y de la respuesta que descarga el archivo.
                output.seek(0)
                response = HttpResponse(
                    output,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename="{nombre}.xlsx"'

                return response
        
            else:

                output = io.StringIO()
                writer = csv.writer(output)

                # Encabezado
                # columnas = ['NumFactura', 'Comprobante', 'Procesamiento', 'Tipo de Comprobante', 'NumComprobante', 'Movimiento', 'Tipo de Imputacion', 'CUIT', 'Cliente', 'Comerciante', 'Importe', 'Neto21', 'IVA21', 'Neto10y5', 'IVA10y5', 'Neto27', 'IVA27', 'ConceptoNoAgrabado', 'PercepcionIVA', 'PercepcionDGR', 'PercepcionMunicipalidad', 'Total']
                columnas = ['CUIT', 'Numero de Factura', 'Tipo de Comprobante', 'Comprobante', 'Importe']
                columnas = ['CUIT', 'Numero de Factura', 'Tipo de Comprobante', 'Comprobante', 'Importe']
                writer.writerow(columnas)

                # Datos
                for dato in datos:
                    writer.writerow([
                        dato.Empresa.CUIT,
                        dato.NFactura,
                        dato.Empresa.CUIT,
                        dato.NFactura,
                        dato.TComprobante,
                        dato.Comprobante,
                        dato.Total
                        dato.Total
                    ])

                response = HttpResponse(
                    output.getvalue(),
                    content_type='text/csv'
                )

                response['Content-Disposition'] = f'attachment; filename="{nombre}.csv"'

                return response



    return render(request, "generar_archivos.html")

##########################################################

########################################################## OCR

def ocr_subir_factura(request):
    """
    Vista unificada: 
    - Subir la factura
    - Extraer datos con OCR
    - Precargar el formulario
    """
    # if request.method == "POST" and request.FILES.get("imagen"):
    if request.method == "POST":
        imagen = request.FILES["imagen"]

        # Guardar imagen temporal
        temp_path = f"temp_{imagen.name}"
        with open(temp_path, "wb+") as destino:
            for chunk in imagen.chunks():
                destino.write(chunk)

        try:
            resultado = procesar_ocr_api(temp_path)

            # Extraer campos importantes
            numero_factura = extraer_numero_factura(resultado)
            fecha_emision_sin_parsear = extraer_fecha_emision(resultado).split('/')
            importe_total = extraer_importe_total(resultado)
            
            fecha_emision = f'{fecha_emision_sin_parsear[2]}-{fecha_emision_sin_parsear[1]}-{fecha_emision_sin_parsear[0]}'

            # Crear formulario precargado con datos OCR
            form = CrearFactura(initial={
                "NFactura": numero_factura,
                "Comprobante": fecha_emision,
                "Total": importe_total,
            }, user=request.user)

            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            print(form)

            return render(request, "cargar_facturas.html", {"form": form})

        except Exception as e:
            print("ERROR EN OCR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    # GET → mostrar formulario vacío
    form = CrearFactura(user=request.user)
    return render(request, "ocr.html", {"form": form})

##########################################################

### Errores comunes al correr en maquinas nuevas ###

# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xab in position 96: invalid start byte
# Falta crear la base de datos (crea una base de datos con el nombre ocDB)

# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf3 in position 85: invalid continuation byte
# Esta mal la clave de la base de datos o el archivo setting.py

import os
import re
from django.shortcuts import render
from django.http import JsonResponse
from .services import procesar_ocr_api




def normalizar_importe(importe_str):
    if not importe_str:
        return None
    limpio = importe_str.replace(".", "").replace(",", ".")
    return limpio





def extraer_numero_factura(texto):
    match = re.search(r"Nro\.?\s*Comp[:\s-]*([0-9]{4}-[0-9]{8})", texto, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None



def extraer_fecha_emision(texto):
    match = re.search(
        r"Fecha\s+de\s+Emisi[oó]n[:\s-]*([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})",
        texto,
        re.IGNORECASE
    )
    return match.group(1).strip() if match else None



def extraer_importe_total(texto):
    """
    Busca el campo 'Importe Total' en el texto del OCR
    y devuelve solo el último número que aparece después.
    """
    lineas = texto.splitlines()
    # Encontrar la línea que contiene "Importe Total"
    for i, linea in enumerate(lineas):
        if "Importe Total" in linea:
            # Tomar todas las líneas siguientes
            siguientes = lineas[i+1:i+10]  # mira las próximas 10 líneas por si hay saltos
            numeros = []
            for lin in siguientes:
                numeros += re.findall(r"[\d\.,]+", lin)
            if numeros:
                # Tomamos solo el último número como Importe Total real
                return normalizar_importe(numeros[-1])
    return None




def ocr_subir_factura(request):
    """
    Vista unificada: 
    - Subir la factura
    - Extraer datos con OCR
    - Precargar el formulario
    """
    # if request.method == "POST" and request.FILES.get("imagen"):
    if request.method == "POST":
        imagen = request.FILES["imagen"]

        # Guardar imagen temporal
        temp_path = f"temp_{imagen.name}"
        with open(temp_path, "wb+") as destino:
            for chunk in imagen.chunks():
                destino.write(chunk)

        try:
            resultado = procesar_ocr_api(temp_path)

            # Extraer campos importantes
            numero_factura = extraer_numero_factura(resultado)
            fecha_emision_sin_parsear = extraer_fecha_emision(resultado).split('/')
            importe_total = extraer_importe_total(resultado)
            
            fecha_emision = f'{fecha_emision_sin_parsear[2]}-{fecha_emision_sin_parsear[1]}-{fecha_emision_sin_parsear[0]}'

            # Crear formulario precargado con datos OCR
            form = CrearFactura(initial={
                "NFactura": numero_factura,
                "Comprobante": fecha_emision,
                "Total": importe_total,
            }, user=request.user)

            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            print(form)

            return render(request, "cargar_facturas.html", {"form": form})

        except Exception as e:
            print("ERROR EN OCR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    # GET → mostrar formulario vacío
    form = CrearFactura(user=request.user)
    return render(request, "ocr.html", {"form": form})