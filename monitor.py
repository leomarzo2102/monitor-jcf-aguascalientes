import os
import requests
from bs4 import BeautifulSoup

# Leemos las credenciales guardadas de forma segura en GitHub
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    """Envía la notificación directamente a tu Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": mensaje, 
        "parse_mode": "Markdown"
    }
    try:
        respuesta = requests.post(url, json=payload)
        print(f"Respuesta del servidor de Telegram: {respuesta.status_code}")
        if respuesta.status_code != 200:
            print(f"Detalle del error de Telegram: {respuesta.text}")
    except Exception as e:
        print(f"Error crítico al conectar con Telegram: {e}")

def revisar_convocatoria():
    url = "https://jovenesconstruyendoelfuturo.stps.gob.mx/focalizacion/"
    # Fingimos ser un navegador normal para evitar bloqueos de seguridad
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        respuesta = requests.get(url, headers=headers, timeout=15)
        print(f"Conexión a la página web del JCF exitosa. Código de estado: {respuesta.status_code}")
        
        # --- MENSAJE DE PRUEBA FORZADO ---
        # Remueve o comenta esta sección una vez que confirmes que te llega al celular
        mensaje_prueba = "🧪 *¡PRUEBA DE CONEXIÓN!* Tu bot de monitoreo en GitHub se ejecutó correctamente y el enlace con Telegram funciona a la perfección. ¡Estamos listos!"
        enviar_telegram(mensaje_prueba)
        # ---------------------------------
              
    except Exception as e:
        print(f"Ocurrió un error al intentar conectar con la web de JCF: {e}")

if __name__ == "__main__":
    # Verificamos si GitHub configuró bien los secretos antes de arrancar
    if not TOKEN_TELEGRAM or not CHAT_ID:
        print(f"❌ ERROR: Faltan configurar las variables en los Secrets de GitHub.")
        print(f"¿TOKEN_TELEGRAM detectado?: {bool(TOKEN_TELEGRAM)}")
        print(f"¿TELEGRAM_CHAT_ID detectado?: {bool(CHAT_ID)}")
    else:
        print("Variables detectadas correctamente. Iniciando monitor...")
        revisar_convocatoria()
