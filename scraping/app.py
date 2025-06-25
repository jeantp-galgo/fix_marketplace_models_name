import requests
from bs4 import BeautifulSoup
import time
import re
from typing import Optional, Dict, Any

class WebScraper:
    """
    Clase básica para extraer texto de páginas web
    """

    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        Inicializa el scraper con headers personalizados

        Args:
            headers: Headers HTTP personalizados para las peticiones
        """
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)
        else:
            # Headers por defecto para simular un navegador
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

    def get_page_content(self, url: str, delay: float = 1.0) -> Optional[str]:
        """
        Obtiene el contenido HTML de una página web

        Args:
            url: URL de la página a scrapear
            delay: Tiempo de espera entre peticiones (en segundos)

        Returns:
            Contenido HTML de la página o None si hay error
        """
        try:
            time.sleep(delay)  # Pausa para ser respetuoso con el servidor
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error al obtener la página {url}: {e}")
            return None

    def clean_text(self, text: str) -> str:
        """
        Limpia y mejora la legibilidad del texto extraído

        Args:
            text: Texto a limpiar

        Returns:
            Texto limpio y legible
        """
        # Eliminar espacios múltiples y saltos de línea
        text = re.sub(r'\s+', ' ', text)

        # Eliminar espacios al inicio y final
        text = text.strip()

        # Separar palabras que están pegadas (cuando hay cambio de mayúscula a minúscula)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

        # Separar números de letras
        text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
        text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)

        # Normalizar espacios alrededor de puntuación
        text = re.sub(r'\s*([.,!?;:])\s*', r'\1 ', text)

        # Eliminar espacios múltiples nuevamente
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def extract_text(self, html_content: str, selector: Optional[str] = None) -> str:
        """
        Extrae texto del contenido HTML

        Args:
            html_content: Contenido HTML de la página
            selector: Selector CSS para extraer texto específico

        Returns:
            Texto extraído y limpio de la página
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            if selector:
                # Extraer texto de elementos específicos usando selector CSS
                elements = soup.select(selector)
                text_parts = [elem.get_text(strip=True) for elem in elements]
                raw_text = ' '.join(text_parts)
            else:
                # Extraer todo el texto de la página
                raw_text = soup.get_text(strip=True)

            # Aplicar limpieza al texto extraído
            return self.clean_text(raw_text)

        except Exception as e:
            print(f"Error al procesar el HTML: {e}")
            return ""

    def scrape_page(self, url: str, selector: Optional[str] = None, delay: float = 1.0) -> Dict[str, Any]:
        """
        Método principal para scrapear una página web

        Args:
            url: URL de la página a scrapear
            selector: Selector CSS opcional para extraer texto específico
            delay: Tiempo de espera entre peticiones

        Returns:
            Diccionario con el resultado del scraping
        """
        result = {
            'url': url,
            'success': False,
            'text': '',
            'error': None
        }

        html_content = self.get_page_content(url, delay)
        if html_content:
            result['text'] = self.extract_text(html_content, selector)
            result['success'] = True
        else:
            result['error'] = 'No se pudo obtener el contenido de la página'

        return result

# Función de utilidad para uso rápido
def quick_scrape(url: str, selector: Optional[str] = None) -> str:
    """
    Función de utilidad para scrapear rápidamente una página

    Args:
        url: URL de la página a scrapear
        selector: Selector CSS opcional

    Returns:
        Texto extraído y limpio de la página
    """
    scraper = WebScraper()
    result = scraper.scrape_page(url, selector)
    return result['text'] if result['success'] else ""
