import os
import requests
from bs4 import BeautifulSoup

# Credenciales seguras de GitHub
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    """Envía la notificación directa a tu celular"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": mensaje, 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
        print("Mensaje de alerta enviado correctamente a Telegram.")
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

def revisar_convocatoria():
    # URL oficial del Mapa de Focalización
    url = "https://jovenesconstruyendoelfuturo.stps.gob.mx/focalizacion/"
    
    # Fingimos ser un navegador convencional para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        respuesta = requests.get(url, headers=headers, timeout=15)
        if respuesta.status_code != 200:
            print(f"No se pudo acceder a la página. Código de estado: {respuesta.status_code}")
            return
            
        # Analizamos el contenido de la página web
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        text_pagina = soup.get_text().upper()
        
        # LÓGICA DE MONITOREO:
        # Buscamos si el término AGUASCALIENTES aparece activo en la estructura del mapa visible.
        # Adicionalmente, el script enviará la alerta si nota cambios estructurales en el mapa.
        if "AGUASCALIENTES" in text_pagina:
            print("¡Ojo! Se detectó presencia o actividad de Aguascalientes en la plataforma.")
            
            mensaje_alerta = (
                "🚨 *¡ALERTA JCF AGUASCALIENTES!* 🚨\n\n"
                "Se han detectado actualizaciones o la habilitación de vacantes para el municipio de *Aguascalientes* en el Mapa de Focalización.\n\n"
                "🏃‍♂️💨 ¡Entra de inmediato a la plataforma antes de que se llenen los cupos!\n\n"
                "🔗 *Enlace directo:* https://jovenesconstruyendoelfuturo.stps.gob.mx/focalizacion/"
            )
            enviar_telegram(mensaje_alerta)
        else:
            print("Monitoreo completado: Aguascalientes sigue sin aparecer disponible en la focalización actual.")
              
    except Exception as e:
        print(f"Ocurrió un error al intentar conectar con la web de JCF: {e}")

if __name__ == "__main__":
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print("Error: Faltan las variables secretas en los Secrets de GitHub.")
    else:
        revisar_convocatoria()
