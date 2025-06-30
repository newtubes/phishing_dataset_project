import json
import os
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN ---
INPUT_DATASET_FILE = "urlscan_phishing_dataset.jsonl"
LABELED_DATASET_FILE = "labeled_phishing_dataset.jsonl"

# --- FUNCIONES ---

def get_user_input(prompt_text):
    """Obtiene una respuesta de sí o no del usuario."""
    while True:
        response = input(prompt_text).lower().strip()
        if response in ['s', 'si', 'sí']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Respuesta no válida. Por favor, introduce 's' para sí o 'n' para no.")

def start_labeling_session():
    """Inicia una sesión interactiva para etiquetar el dataset."""
    if not os.path.exists(INPUT_DATASET_FILE):
        print(f"¡Error! No se encontró el archivo de datos '{INPUT_DATASET_FILE}'.")
        print("Asegúrate de haber ejecutado 'fetch_phish.py' con éxito.")
        return

    with open(INPUT_DATASET_FILE, 'r', encoding='utf-8') as f:
        entries = [json.loads(line) for line in f]

    print("--- Iniciando Sesión de Etiquetado (Versión Mejorada) ---")
    print(f"Se encontraron {len(entries)} entradas para revisar.")
    print(f"Los datos etiquetados se guardarán en '{LABELED_DATASET_FILE}'.\n")

    labeled_count = 0
    with open(LABELED_DATASET_FILE, 'w', encoding='utf-8') as out_file:
        for i, entry in enumerate(entries):
            print(f"--- Revisando Entrada {i + 1}/{len(entries)} ---")
            print(f"URL Original: {entry.get('original_url')}")

            html_content = entry.get('texto_de_la_pagina', '')

            if not html_content:
                print("No hay contenido HTML en esta entrada. Saltando.")
                out_file.write(json.dumps(entry) + '\n')
                print("-------------------------------------\n")
                continue

            # Usamos BeautifulSoup para extraer el texto de forma inteligente
            soup = BeautifulSoup(html_content, 'lxml')
            visible_text = soup.get_text(separator='\n', strip=True)

            if not visible_text or len(visible_text.strip()) < 50:
                print("No se encontró texto significativo en esta página. Saltando.")
                out_file.write(json.dumps(entry) + '\n')
                print("-------------------------------------\n")
                continue

            labeled_count += 1
            print("\n--- Texto Extraído de la Página ---")
            print(visible_text[:2000]) # Mostramos hasta 2000 caracteres
            print("----------------------------------\n")

            entry['tacticas_sociales']['falsa_urgencia'] = get_user_input("¿Contiene 'falsa urgencia'? (ej. 'actúa ahora', 'tiempo limitado') (s/n): ")
            entry['tacticas_sociales']['apelacion_a_la_autoridad'] = get_user_input("¿Contiene 'apelación a la autoridad'? (ej. 'de parte de Microsoft', 'aviso del banco') (s/n): ")
            entry['tacticas_sociales']['curiosidad_cebo_de_clic'] = get_user_input("¿Contiene 'cebo de curiosidad'? (ej. 'mira este video vergonzoso') (s/n): ")
            entry['tacticas_sociales']['miedo_cuenta_comprometida'] = get_user_input("¿Contiene 'miedo o amenaza'? (ej. 'actividad sospechosa en tu cuenta') (s/n): ")
            entry['tacticas_sociales']['oportunidad_falso_premio'] = get_user_input("¿Contiene 'oportunidad o premio falso'? (ej. 'has ganado la lotería') (s/n): ")
            entry['tacticas_sociales']['error_inesperado'] = get_user_input("¿Contiene un 'error inesperado'? (ej. 'no se pudo entregar el paquete') (s/n): ")

            out_file.write(json.dumps(entry) + '\n')
            print("¡Entrada etiquetada y guardada!")
            print("-------------------------------------\n")

    print("--- Sesión de Etiquetado Finalizada ---")
    if labeled_count == 0:
        print("No se encontró ninguna página con texto suficiente para etiquetar en este lote.")
        print("Puedes probar a ejecutar 'fetch_phish.py' de nuevo para analizar un nuevo conjunto de URLs.")
    else:
        print(f"¡Buen trabajo! Has etiquetado {labeled_count} páginas.")

if __name__ == "__main__":
    start_labeling_session()