import os, re, requests
from datetime import datetime
from decouple import config

def is_valid_fecha(fecha_str, formato="%Y-%m-%d"):

    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False

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


API_URL = config('API_URL')
API_KEY = config('API_KEY')

def procesar_ocr_api(image_path):

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"El archivo no existe: {image_path}")

    with open(image_path, "rb") as f:
        response = requests.post(
            API_URL,
            headers={"apikey": API_KEY},
            files={"file": f},
            data={
                "language": "spa",
                "isOverlayRequired": False
            }
        )

    if response.status_code != 200:
        raise Exception(f"Error en OCR API: {response.status_code} - {response.text}")

    result = response.json()
    # print("DEBUG - Respuesta JSON:", result)

    if result.get("IsErroredOnProcessing"):
        raise Exception(f"OCR falló: {result.get('ErrorMessage')}")

    # 👇 Devolver solo el texto plano, no todo el JSON
    return result["ParsedResults"][0]["ParsedText"]