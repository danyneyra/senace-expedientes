"""
Scraper para extraer URLs de PDFs de las páginas de proyectos
"""
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from config import API_PDF_URL, DOWNLOADS_DIR

class PDFScraperError(Exception):
    """Excepción base para errores del PDFScraper"""
    pass

class PDFDownloadError(PDFScraperError):
    """Error al descargar o acceder a un PDF"""
    pass

class PDFScraper:
    def __init__(self):
        self.session = requests.Session()

    def extract_pdf_url(self, project_url: str) -> str:
        """
        Extrae la URL del PDF de la página del proyecto
        
        Args:
            project_url: URL de la página del proyecto
            
        Returns:
            URL del PDF
            
        Raises:
            PDFDownloadError: Si hay un error al acceder a la página o no se encuentra el PDF
        """
        response = self.session.get(project_url)
        if response.status_code != 200:
            raise PDFDownloadError(f"❌ Error al obtener la página del proyecto: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_name = soup.find("h1", class_="quickshare-node-header-info-title thin dark")
        if not pdf_name:
            raise PDFDownloadError(f"❌ No se encontró el nombre del PDF en {project_url}")
        
        pdf_name = pdf_name.get_text(strip=True)
        
        # Obtener el último segmento del path de la URL
        parsed_url = urlparse(project_url)
        last_path_segment = parsed_url.path.strip("/").split("/")[-1]

        # Construir la URL final
        url_pdf = f"{API_PDF_URL}{last_path_segment}/content/{pdf_name}"

        return url_pdf

    def download_pdf(self, pdf_url: str) -> bool:
        """
        Descarga un PDF y lo guarda en la carpeta de descargas
        
        Args:
            pdf_url: URL del PDF a descargar
            
        Returns:
            True si la descarga fue exitosa, False en caso contrario
            
        Raises:
            PDFDownloadError: Si hay un error al descargar o guardar el PDF
        """
        try:
            response = self.session.get(pdf_url, stream=True)
            if response.status_code != 200:
                raise PDFDownloadError(f"❌ Error al descargar el PDF: {response.status_code}")

            # Extraer el nombre del archivo de la URL
            filename = os.path.basename(pdf_url)
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Crear el directorio de descargas si no existe
            os.makedirs(DOWNLOADS_DIR, exist_ok=True)
            
            # Ruta completa del archivo
            output_path = os.path.join(DOWNLOADS_DIR, filename)
            
            # Guardar el PDF
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
            
        except requests.RequestException as e:
            raise PDFDownloadError(f"❌ Error en la descarga: {str(e)}")
        except IOError as e:
            raise PDFDownloadError(f"❌ Error al guardar el archivo: {str(e)}")

    def close(self):
        self.session.close()
