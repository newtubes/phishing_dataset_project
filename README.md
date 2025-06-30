# Proyecto de Dataset de Phishing by Rebeca Romcy

Este proyecto está diseñado para recolectar, analizar y etiquetar URLs de phishing para crear un dataset de alta calidad. El objetivo final es utilizar este dataset para entrenar modelos de IA capaces de detectar tácticas de ingeniería social en texto.

## Características

*   **Recolección de Datos:** Utiliza la API de [urlscan.io](https://urlscan.io/) y la fuente de [OpenPhish](https://openphish.com/) para obtener URLs de phishing activas.
*   **Análisis de Páginas:** Extrae el contenido DOM (texto) de las páginas de phishing para su posterior análisis.
*   **Etiquetado Interactivo:** Proporciona un script para que un humano pueda etiquetar las tácticas de ingeniería social presentes en cada página.
*   **Estructura Organizada:** El código está organizado en un directorio `src` para mayor claridad.

## Cómo Empezar

### Prerrequisitos

*   Python 3.x
*   Las librerías de Python listadas en `requirements.txt` (puedes instalarlas con `pip install -r requirements.txt`).

### Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd phishing_dataset_project
    ```

2.  **Obtén una clave de API:**
    *   Ve a [urlscan.io](https://urlscan.io/user/profile/) y obtén tu clave de API.
    *   Abre los archivos en el directorio `src` y reemplaza el placeholder `"TU_CLAVE_DE_API_DE_URLSCAN_AQUI"` con tu clave real.

### Uso

1.  **Recolectar Datos:**
    *   Para buscar análisis de phishing recientes y de alta calidad (recomendado):
        ```bash
        python src/search_scans.py
        ```
    *   Para buscar URLs en una fuente en tiempo real y analizarlas desde cero:
        ```bash
        python src/fetch_phish.py
        ```
    Ambos scripts guardarán sus resultados en `urlscan_phishing_dataset.jsonl`.

2.  **Etiquetar los Datos:**
    *   Una vez que tengas datos en `urlscan_phishing_dataset.jsonl`, ejecuta el script de etiquetado:
        ```bash
        python src/label_data.py
        ```
    *   Sigue las instrucciones en la consola para clasificar cada página. Los resultados se guardarán en `labeled_phishing_dataset.jsonl`.

## Estructura del Proyecto

*   `src/`: Contiene el código fuente de Python.
    *   `fetch_phish.py`: Obtiene URLs de OpenPhish y las analiza.
    *   `search_scans.py`: Busca análisis ya existentes en urlscan.io.
    *   `label_data.py`: Script interactivo para el etiquetado de datos.
*   `urlscan_phishing_dataset.jsonl`: Datos crudos descargados (sin etiquetar).
*   `labeled_phishing_dataset.jsonl`: Datos etiquetados por el usuario.
*   `README.md`: Este archivo.

## Contribuciones

Este es un proyecto personal para mi portafolio, pero estoy abierto a sugerencias y mejoras. Si tienes alguna idea, no dudes en abrir un *issue*.
