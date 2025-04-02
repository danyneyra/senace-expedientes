"""
Cliente para interactuar con la API de SENACE
"""
import requests
from typing import Dict, List, Optional, Tuple
from typing_extensions import Literal
import json
from datetime import datetime
from pathlib import Path
from config import TEMP_DIR, API_BASE_URL
import unicodedata

# Definición de tipos literales
SectorType = Literal[
    "Agricultura y Riego",
    "Energía y Minas",
    "Salud",
    "Senace",
    "Transportes y Comunicaciones",
    "Vivienda, Construcción y Saneamiento"
]

TipoEstudioType = Literal[
    "Actualización",
    "Clasificación",
    "Cls Anticipada",
    "DIA",
    "EIA",
    "EIA-d",
    "EIA-sd",
    "IGAPRO",
    "IntegrAmbiente",
    "ITS",
    "MEIA-d",
    "MEIA-sd",
    "PMA",
    "PPC",
    "TdR"
]

EstadoType = Literal[
    "Aprobado",
    "Conforme"
]

# Lista de valores válidos para referencia
SECTORES: List[SectorType] = [
    "Agricultura y Riego",
    "Energía y Minas",
    "Salud",
    "Senace",
    "Transportes y Comunicaciones",
    "Vivienda, Construcción y Saneamiento"
]

TIPOS_ESTUDIO: List[TipoEstudioType] = [
    "Actualización",
    "Clasificación",
    "Cls Anticipada",
    "DIA",
    "EIA",
    "EIA-d",
    "EIA-sd",
    "IGAPRO",
    "IntegrAmbiente",
    "ITS",
    "MEIA-d",
    "MEIA-sd",
    "PMA",
    "PPC",
    "TdR"
]

class SenaceClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.temp_dir = TEMP_DIR
        self.max_records_per_page = 2000

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normaliza el texto removiendo acentos y convirtiendo a minúsculas
        
        Args:
            text: Texto a normalizar
            
        Returns:
            Texto normalizado sin acentos y en minúsculas
        """
        normalized = unicodedata.normalize('NFKD', text)
        ascii_text = normalized.encode('ASCII', 'ignore').decode('ASCII')
        return ascii_text.lower()

    def get_sectors(self) -> List[SectorType]:
        """Obtiene la lista de sectores disponibles"""
        return SECTORES

    def get_tipos_estudio(self) -> List[TipoEstudioType]:
        """Obtiene la lista de tipos de estudio disponibles"""
        return TIPOS_ESTUDIO

    def _get_total_count(self, where_clause: str) -> int:
        """
        Obtiene el número total de registros para una consulta
        
        Args:
            where_clause: Cláusula WHERE de la consulta
            
        Returns:
            Número total de registros
        """
        count_params = {
            "f": "json",
            "where": where_clause,
            "returnCountOnly": "true"
        }
        
        response = self.session.get(self.base_url, params=count_params)
        response.raise_for_status()
        
        if response.status_code != 200:
            print("❌ Error al obtener el conteo:", response.status_code)
            return 0
            
        data = response.json()
        return data.get('count', 0)

    def _make_request(self, params: Dict) -> List[Dict]:
        """
        Realiza una petición a la API y devuelve los resultados
        
        Args:
            params: Parámetros de la consulta
            
        Returns:
            Lista de resultados
        """
        response = self.session.get(self.base_url, params=params)
        response.raise_for_status()

        if response.status_code != 200:
            print("❌ Error en la petición:", response.status_code)
            return []
        
        data = response.json()
        return data.get('features', [])

    def search_projects(self, 
                       sector: Optional[SectorType] = None,
                       tipo_estudio: Optional[TipoEstudioType] = None,
                       nombre_proyecto: Optional[str] = None,
                       fecha_inicio: Optional[str] = None,
                       fecha_fin: Optional[str] = None,
                       estado: Optional[EstadoType] = None) -> List[Dict]:
        """
        Busca proyectos según los filtros especificados

        Args:
            sector: Sector del proyecto
            tipo_estudio: Tipo de estudio
            nombre_proyecto: Nombre del proyecto
            fecha_inicio: Fecha de inicio en formato YYYY-MM-DD
            fecha_fin: Fecha fin en formato YYYY-MM-DD
            estado: Estado del proyecto

        Returns:
            Lista de proyectos que coinciden con los criterios de búsqueda
        """
        base_params = {
            "f": "json",
            "where": "1=1",
            "returnGeometry": "false",
            "spatialRel": "esriSpatialRelIntersects",
            "outFields": ",".join([
                "OBJECTID", "EXPEDIENTE", "SECTOR", "ACTIVIDAD", "DIRECCION", 
                "NOM_PROY", "UNIDAD_PROY", "IGA_TIPO", "IGA_TIPO_DET", "TIT_PROY",
                "RUC_TITULAR", "ESTADO_GEN", "ESTADO_DET", "FECHA_ING", "FECHA_RD",
                "NRO_RD", "CONSULTORA", "RUC_CONSULT", "MONTO_INV", "MONEDA_INV",
                "VER_RESOLU", "VER_ESTUDIO", "VER_INFORME", "VER_RESUME", "VER_EVA",
                "VER_OPINI", "VER_MAPAS", "LONGITUD", "LATITUD", "RCA"
            ]),
            "outSR": "102100",
            "resultOffset": "0",
            "resultRecordCount": str(self.max_records_per_page)
        }

        # Construir la consulta WHERE
        where_clauses = []
        
        if sector:
            where_clauses.append(f"SECTOR = '{sector}'")

        if tipo_estudio:
            where_clauses.append(f"IGA_TIPO = '{tipo_estudio}'")

        if nombre_proyecto:
            nombre_normalizado = self.normalize_text(nombre_proyecto)
            variantes = [
                nombre_proyecto,  # Original
                nombre_normalizado,  # Sin tildes en minúsculas
                nombre_proyecto.upper(),  # Original en mayúsculas
                nombre_normalizado.upper(),  # Sin tildes en mayúsculas
            ]
            nombre_conditions = [f"NOM_PROY LIKE '%{v}%'" for v in variantes]
            where_clauses.append(f"({' OR '.join(nombre_conditions)})")
        
        if fecha_inicio:
            where_clauses.append(f"FECHA_RD >= '{fecha_inicio}'")
        
        if fecha_fin:
            where_clauses.append(f"FECHA_RD <= '{fecha_fin}'")

        if estado:
            where_clauses.append(f"ESTADO_DET = '{estado}'")

        # Construir where final
        where_clause = ' AND '.join(where_clauses) if where_clauses else '1=1'
        base_params['where'] = where_clause

        # Obtener el conteo total primero
        total_count = self._get_total_count(where_clause)
        
        # Obtener primera página
        all_results = []
        first_page = self._make_request(base_params)
        all_results.extend(first_page)

        # Si hay más páginas, obtenerlas
        offset = self.max_records_per_page
        while offset < total_count:
            base_params['resultOffset'] = str(offset)
            page_results = self._make_request(base_params)
            if not page_results:  # Si no hay resultados, salir del bucle
                break
            all_results.extend(page_results)
            print(f"📥 Obtenidos {len(all_results)} de {total_count} registros...")
            offset += self.max_records_per_page

        # Guardar todos los resultados en archivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.temp_dir / f"search_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(all_results, json_file, ensure_ascii=False, indent=4)
        print(f"✅ Datos encontrados ({len(all_results)} de {total_count}) y guardados en {output_file}")
        
        return all_results