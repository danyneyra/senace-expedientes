# SENACE Expedientes Downloader

Aplicación Python para la descarga automatizada de expedientes del SENACE (Servicio Nacional de Certificación Ambiental para las Inversiones Sostenibles) de Perú.

## Características

- Conexión con la API de SENACE
- Filtrado por sectores (Energía y Minas, Agricultura y Riego, Transportes y Comunicaciones, etc.), tipo de estudio, fecha de inicio y finalización, estado, nombre del proyecto
- Búsqueda y descarga automática de PDF de Informe de Estudios

## Requisitos

- Python 3.8+
- Entorno virtual (venv)

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd senace-expedientes
```

2. Activar el entorno virtual:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
senace-expedientes/
├── src/
│   ├── api/
│   │   └── senace_client.py
│   ├── scrapers/
│   │   └── pdf_scraper.py
├── downloads/
├── requirements.txt
├── .gitignore
├── config.py
├── app.py
└── README.md
```

## Uso

[Instrucciones de uso pendientes]

## Licencia

[Tipo de licencia pendiente]
