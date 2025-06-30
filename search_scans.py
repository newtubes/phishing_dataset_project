

import requests
import json
import time
import os

# --- CONFIGURACIÓN ---
# Tu clave de API de URLScan.io
URLSCAN_API_KEY = "0197bccf-6046-728f-981a-c94e6406f27d"

# Archivo para guardar nuestro dataset
DATASET_FILE = "urlscan_phishing_dataset.jsonl"

# --- FUNCIONES ---

def search_for_phishing_scans():
    """Busca en URLScan.io los análisis recientes etiquetados como phishing."""
    print("Buscando en URLScan.io análisis de phishing recientes...")
    headers = {'API-Key': URLSCAN_API_KEY}
    # Buscamos scans de las últimas 24 horas que tengan la etiqueta 'phishing'
    # y que tengan un DOM guardado.
    query = "tags:phishing AND date:>now-24h AND has_dom:true"
    params = {'q': query, 'size': 100} # Pedimos 100 resultados

    try:
        response = requests.get('https://urlscan.io/api/v1/search/', headers=headers, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])
        print(f"Búsqueda exitosa. Se encontraron {len(results)} análisis relevantes.")
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar en URLScan.io: {e}")
        return []

def fetch_scan_result(result_api_url):
    """Descarga el resultado completo de un análisis específico."""
    print(f"Descargando resultado desde: {result_api_url}")
    try:
        response = requests.get(result_api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el resultado del análisis: {e}")
        return None

# --- FUNCIÓN PRINCIPAL ---

def main():
    """Orquesta la búsqueda y guardado de datos de phishing."""
    if URLSCAN_API_KEY == "0197bccf-6046-728f-981a-c94e6406f27d":
        print("¡ERROR! Por favor, edita el archivo 'search_scans.py' y añade tu clave de API de URLScan.io.")
        return

    # Borramos el archivo viejo para empezar de cero con datos de calidad
    if os.path.exists(DATASET_FILE):
        print(f"Borrando el archivo de datos antiguo: {DATASET_FILE}")
        os.remove(DATASET_FILE)

    scans = search_for_phishing_scans()
    if not scans:
        print("No se encontraron análisis recientes. Inténtalo de nuevo más tarde.")
        return

    for scan_info in scans:
        result_url = scan_info.get('result')
        if not result_url:
            continue

        scan_result = fetch_scan_result(result_url)
        if not scan_result:
            continue

        page_info = scan_result.get("page", {})
        dom_content = scan_result.get("data", {}).get("dom", "")

        # Solo guardamos si tenemos el contenido del DOM
        if dom_content:
            tactics = {
                "falsa_urgencia": False, "apelacion_a_la_autoridad": False,
                "curiosidad_cebo_de_clic": False, "miedo_cuenta_comprometida": False,
                "oportunidad_falso_premio": False, "error_inesperado": False
            }

            structured_entry = {
                "scan_id": scan_result.get("task", {}).get("uuid"),
                "original_url": page_info.get("url"),
                "dominio": page_info.get("domain"),
                "ip": page_info.get("ip"),
                "pais_servidor": page_info.get("country"),
                "texto_de_la_pagina": dom_content,
                "tacticas_sociales": tactics,
                "fuente": "URLScan.io Search"
            }

            with open(DATASET_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps(structured_entry) + '\n')
            print(f"Guardado análisis para: {page_info.get('url')}")
        
        time.sleep(2) # Pausa para no saturar la API

    print("\nProceso de recolección finalizado.")
    print(f"Los nuevos datos están listos en '{DATASET_FILE}'.")
    print("Ahora puedes ejecutar 'python label_data.py' para empezar a etiquetar.")

if __name__ == "__main__":
    main()
