from src.api.senace_client import SenaceClient
from config import API_BASE_URL
from src.scrapers.pdf_scraper import PDFScraper, PDFDownloadError
import re

client = SenaceClient(API_BASE_URL)

# Obtener sectores y tipos de estudio
# sectores = client.get_sectors()
# tipos_estudio = client.get_tipos_estudio()

# Buscar proyectos
proyectos = client.search_projects(sector="Energía y Minas", fecha_inicio='2020-01-01', estado="Aprobado", nombre_proyecto="Exploración")

# Obtener URL de Informe de Estudios
for proyecto in proyectos:
    attributes = proyecto.get('attributes')
    url = attributes.get('VER_ESTUDIO')
    
    # Corregir URL si viene mal formada
    if url.startswith('ttp://'):
        url = 'h' + url
    elif not url.startswith(('http://', 'https://')):
        print(f"❌ URL inválida para el expediente {attributes.get('EXPEDIENTE')}: {url}")
        continue

    scraper = PDFScraper()
    try:
        pdf_url = scraper.extract_pdf_url(url)
        success = scraper.download_pdf(pdf_url)
        if success:
            print(f"✅ PDF descargado correctamente del expediente: {attributes.get('EXPEDIENTE')}")
    except PDFDownloadError as e:
        print(f"❌ Error en expediente {attributes.get('EXPEDIENTE')}: {e}")
    finally:
        scraper.close()