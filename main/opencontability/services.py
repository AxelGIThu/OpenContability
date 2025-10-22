import requests
import os


API_URL = "https://api.ocr.space/parse/image"
API_KEY = os.getenv("API_KEY", "K83953885188957")


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

