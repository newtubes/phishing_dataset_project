import requests
import json
import time
import os

# --- CONFIGURACIÓN ---
# TU CLAVE API VA AQUI
# La puedes obtener en: https://urlscan.io/user/profile/
URLSCAN_API_KEY = "TU CLAVE API VA AQUI"

# Fuente de URLs de phishing (no requiere clave)
OPENPHISH_FEED_URL = "https://openphish.com/feed.txt"

# Archivo para guardar nuestro dataset
DATASET_FILE = "urlscan_phishing_dataset.jsonl"

# --- FUNCIONES DE LA API ---

def get_latest_phishing_urls():
    """Obtiene la lista más reciente de URLs de phishing de OpenPhish."""
    print("Descargando URLs de phishing desde OpenPhish...")
    try:
        response = requests.get(OPENPHISH_FEED_URL)
        response.raise_for_status()
        urls = response.text.strip().split('\n')
        print(f"Se encontraron {len(urls)} URLs.")
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la lista de URLs: {e}")
        return []

def submit_url_to_scan(url_to_scan):
    """Envía una URL a URLScan.io para que sea analizada."""
    headers = {
        'API-Key': URLSCAN_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {"url": url_to_scan, "visibility": "public"}
    
    print(f"Enviando URL a URLScan.io: {url_to_scan}")
    try:
        response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("¡URL enviada con éxito!")
            return response.json()
        else:
            print(f"Error al enviar URL. Estado: {response.status_code}, Respuesta: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al enviar a URLScan: {e}")
        return None

def get_scan_results(result_api_url):
    """Consulta la API de resultados de URLScan hasta que el análisis esté completo."""
    print(f"Esperando resultados de la API: {result_api_url}")
    # Esperamos un poco antes de la primera consulta
    time.sleep(15)
    
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        try:
            response = requests.get(result_api_url)
            if response.status_code == 200:
                print("¡Resultados del análisis recibidos!")
                return response.json()
            elif response.status_code == 404:
                print(f"El análisis aún no está listo. Reintentando en 10 segundos... (Intento {attempts + 1}/{max_attempts})")
                attempts += 1
                time.sleep(10)
            else:
                print(f"Error al obtener resultados. Estado: {response.status_code}, Respuesta: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al obtener resultados: {e}")
            return None
            
    print("Se superó el número de reintentos. El análisis podría estar tardando demasiado.")
    return None

# --- FUNCIÓN PRINCIPAL ---

def main():
    """Orquesta todo el proceso de recolección y guardado de datos."""
    if URLSCAN_API_KEY == "TU_CLAVE_DE_API_DE_URLSCAN_AQUI":
        print("¡ERROR! Por favor, edita el archivo 'fetch_phish.py' y añade tu clave de API de URLScan.io.")
        return

    phishing_urls = get_latest_phishing_urls()
    if not phishing_urls:
        return

            # Limitamos a 100 URLs para esta ejecución
    urls_to_process = phishing_urls[:100]
    print(f"\nProcesando las primeras {len(urls_to_process)} URLs como prueba.")

    for url in urls_to_process:
        submission_data = submit_url_to_scan(url)
        
        if submission_data and 'api' in submission_data:
            result_url = submission_data['api']
            scan_result = get_scan_results(result_url)
            
            if scan_result:
                # Aquí extraemos solo la información que nos interesa
                page_info = scan_result.get("page", {})
                
                # Tácticas de ingeniería social (nuestro objetivo final)
                tactics = {
                    "falsa_urgencia": False,
                    "apelacion_a_la_autoridad": False,
                    "curiosidad_cebo_de_clic": False,
                    "miedo_cuenta_comprometida": False,
                    "oportunidad_falso_premio": False,
                    "error_inesperado": False
                }

                structured_entry = {
                    "scan_id": scan_result.get("task", {}).get("uuid"),
                    "original_url": url,
                    "url_analizada": page_info.get("url"),
                    "dominio": page_info.get("domain"),
                    "ip": page_info.get("ip"),
                    "pais_servidor": page_info.get("country"),
                    "texto_de_la_pagina": scan_result.get("data", {}).get("dom", ""), # ¡El texto que necesitamos!
                    "tacticas_sociales": tactics, # El campo que llenaremos después
                    "fuente": "OpenPhish / URLScan.io"
                }
                
                # Guardamos la entrada en formato JSONL (una línea por JSON)
                with open(DATASET_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(structured_entry) + '\n')
                
                print(f"¡Datos de {url} guardados en {DATASET_FILE}!\n")
        
        # Pausa para no saturar la API
        time.sleep(5)

    print("Proceso de recolección de prueba finalizado.")

if __name__ == "__main__":
    main()
