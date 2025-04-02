"""
Configuración global del proyecto
"""
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
TEMP_DIR = BASE_DIR / "temp"

# Asegurar que los directorios existan
DOWNLOADS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Configuración de la API
API_BASE_URL = "https://services6.arcgis.com/JveWadtaHNLCMyKC/arcgis/rest/services/IGA_SENACE_WEB/FeatureServer/20/query"
API_PDF_URL = "http://ceropapel.senace.gob.pe/share/proxy/alfresco-noauth/api/internal/shared/node/"
API_TIMEOUT = 30  # segundos