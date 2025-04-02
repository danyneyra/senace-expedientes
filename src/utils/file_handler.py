"""
Utilidades para el manejo de archivos y directorios
"""
import os
from pathlib import Path
from typing import Optional

class FileHandler:
    def __init__(self, base_dir: str = "downloads"):
        self.base_dir = Path(base_dir)
        self._ensure_base_dir()

    def _ensure_base_dir(self):
        """Asegura que el directorio base exista"""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_sector_path(self, sector: str) -> Path:
        """Obtiene la ruta para un sector específico"""
        sector_path = self.base_dir / sector
        sector_path.mkdir(parents=True, exist_ok=True)
        return sector_path

    def generate_filename(self, 
                         original_name: str, 
                         sector: str,
                         project_id: Optional[str] = None) -> Path:
        """Genera un nombre de archivo único y organizado"""
        pass
