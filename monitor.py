import os
import requests
from bs4 import BeautifulSoup

TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

def revisar_convocatoria():
    url = "https://jovenesconstruyendoelfuturo.stps.gob.mx/focalizacion/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        respuesta = requests.get(url, headers=headers, timeout=15)
        if respuesta.status_code != 200:
            print(f"Error de acceso. Código: {respuesta.status_code}")
            return

        soup = BeautifulSoup(respuesta.text, 'html.parser')
        text_pagina = soup.get_text().upper()

        # Buscamos si la palabra AGUASCALIENTES está activa en el texto o mapa
        if "AGUASCALIENTES" in text_pagina:
            mensaje = "🚨 *¡ALERTA JCF AGUASCALIENTES!* Se detectaron cambios en el Mapa de Focalización. ¡Revisa la plataforma de inmediato! 🏃‍♂️💨\n\n🔗 https://jovenesconstruyendoelfuturo.stps.gob.mx/focalizacion/"
            enviar_telegram(mensaje)
            print("¡Alerta enviada a Telegram!")
        else:
            print("Aguascalientes sigue sin aparecer en la focalización actual.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Error: Faltan las variables secretas en GitHub.")
    else:
        revisar_convocatoria()
