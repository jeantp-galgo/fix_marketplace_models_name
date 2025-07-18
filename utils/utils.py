from bs4 import BeautifulSoup

def leer_html(ruta_html):
    """Lee un archivo HTML y extrae solo el texto limpio, sin etiquetas."""
    try:
        with open(ruta_html, 'r', encoding='utf-8') as archivo_html:
            contenido_html = archivo_html.read()

            # Parsear el HTML y extraer solo el texto
            soup = BeautifulSoup(contenido_html, 'html.parser')
            texto_limpio = soup.get_text(separator="\n", strip=True)  # Extraer texto con saltos de línea

            return texto_limpio  # Devuelve el texto limpio
    except FileNotFoundError:
        print(f"El archivo {ruta_html} no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo HTML: {e}")
        return None

def leer_html_puro(ruta_html):
    """Lee un archivo HTML y extrae solo el texto limpio, sin etiquetas."""
    try:
        with open(ruta_html, 'r', encoding='utf-8') as archivo_html:
            contenido_html = archivo_html.read()

            return contenido_html  # Devuelve el texto limpio
    except FileNotFoundError:
        print(f"El archivo {ruta_html} no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo HTML: {e}")
        return None

def eliminar_clases_html(html, clases_a_eliminar=None, clases_a_conservar=None):
    """
    Elimina del HTML todos los elementos que tengan las clases especificadas en 'clases_a_eliminar'.
    Alternativamente, si se especifica 'clases_a_conservar', extrae solo los elementos con esas clases y sus contenidos.
    Si ambos son None, retorna el HTML original.

    Parámetros:
    - html: str, el HTML de entrada.
    - clases_a_eliminar: list[str] o None, lista de clases a eliminar.
    - clases_a_conservar: list[str] o None, lista de clases a conservar (extrae solo esos elementos).

    Retorna:
    - str, el HTML modificado.
    """
    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    if clases_a_eliminar:
        # Eliminar todos los elementos que tengan alguna de las clases a eliminar
        for clase in clases_a_eliminar:
            # Buscar todos los elementos con la clase y eliminarlos
            for tag in soup.find_all(class_=clase):
                tag.decompose()  # Elimina el tag del árbol
        return str(soup)
    elif clases_a_conservar:
        # Extraer solo los elementos que tengan alguna de las clases a conservar
        elementos_conservados = []
        for clase in clases_a_conservar:
            # Buscar todos los elementos con la clase a conservar
            elementos_conservados.extend(soup.find_all(class_=clase))
        # Si no se encontró nada, retornar string vacío
        if not elementos_conservados:
            return ""
        # Unir el HTML de todos los elementos encontrados
        # NOTA: Si quieres solo el texto, puedes usar .get_text() en vez de str()
        return "\n".join(str(elem) for elem in elementos_conservados)
    # Si no se especifica nada, retornar el HTML original
    return str(soup)


import re

def limpiar_texto_modelos(texto):
    """
    Elimina precios, palabras no deseadas y saltos de línea vacíos del texto de modelos.
    """

    # Lista de palabras/frases a eliminar (agregar más según necesites)
    palabras_a_eliminar = [
        # intención de compras

        'promociones', "promo", "ver moto", "separar"

        # Precios y monedas
        'precio', 'price', 'costo', 'cost', 'valor', 'value',
        'desde', 'from', 'starting', 'a partir de',
        'financiamiento', 'financing', 'crédito', 'credit',
        'contado', 'cash', 'efectivo',

        # Disponibilidad y stock
        'disponible', 'available', 'stock', 'inventario', 'inventory',
        'agotado', 'out of stock', 'sin stock', 'no disponible',
        'próximamente', 'coming soon', 'en camino',

        # Promociones y ofertas
        'oferta', 'offer', 'descuento', 'discount', 'promoción', 'promotion',
        'especial', 'special', 'liquidación', 'clearance',
        'rebaja', 'sale', 'outlet',

        # Términos comerciales
        'nuevo', 'new', 'usado', 'used', 'seminuevo', 'pre-owned',
        'garantía', 'warranty', 'servicio', 'service',
        'repuestos', 'parts', 'accesorios', 'accessories',

        # Ubicaciones comunes
        'bogotá', 'medellín', 'cali', 'barranquilla', 'cartagena',
        'ciudad de méxico', 'guadalajara', 'monterrey', 'puebla',
        'santiago', 'valparaíso', 'concepción', 'antofagasta',

        # Términos técnicos que no son modelo
        'cilindrada', 'cc', 'hp', 'cv', 'rpm', 'torque',
        'manual', 'automático', 'mecánico', 'eléctrico',

        # Palabras de navegación web
        'ver más', 'see more', 'detalles', 'details', 'información',
        'contacto', 'contact', 'cotizar', 'quote', 'solicitar',
        'comprar', 'buy', 'agregar', 'add', 'carrito', 'cart'
    ]

    # Paso 1: Eliminar precios con formato de moneda
    patron_precios = r'(\$|MXN|COP|CLP|USD|EUR|PEN|ARS)\s?\d{1,3}(?:[,.\s]\d{3})*(?:[,.\s]\d{2})?'
    texto_sin_precios = re.sub(patron_precios, '', texto, flags=re.IGNORECASE)

    # Paso 2: Eliminar números sueltos que parecen precios (ej: 5.700.000)
    patron_numeros_grandes = r'\b\d{1,3}(?:[,.\s]\d{3}){2,}\b'
    texto_sin_numeros = re.sub(patron_numeros_grandes, '', texto_sin_precios)

    # Paso 3: Eliminar palabras no deseadas
    for palabra in palabras_a_eliminar:
        # Buscar la palabra completa (no como parte de otra palabra)
        patron_palabra = r'\b' + re.escape(palabra) + r'\b'.lower()
        texto_sin_numeros = re.sub(patron_palabra, '', texto_sin_numeros, flags=re.IGNORECASE)

    # Paso 4: Limpiar caracteres especiales y espacios extra
    # Eliminar caracteres especiales comunes que no son útiles
    texto_sin_numeros = re.sub(r'[•·▪▫■□●○◆◇★☆]+', '', texto_sin_numeros)
    # Eliminar guiones sueltos
    texto_sin_numeros = re.sub(r'\s-\s', ' ', texto_sin_numeros)
    # Eliminar espacios múltiples
    texto_sin_numeros = re.sub(r'\s+', ' ', texto_sin_numeros)

    # Paso 5: Procesar línea por línea
    lineas = texto_sin_numeros.split('\n')
    lineas_limpias = []

    for linea in lineas:
        # Limpiar espacios al inicio y final
        linea_limpia = linea.strip()

        # Eliminar líneas que son solo números, espacios o caracteres especiales
        if re.match(r'^[\s\d\-.,;:!?()[\]{}"\'+/*=<>@#$%^&|\\~`]*$', linea_limpia):
            continue

        # Eliminar líneas muy cortas (menos de 3 caracteres) que probablemente no son modelos
        if len(linea_limpia) < 3:
            continue

        # Eliminar líneas que son solo años
        if re.match(r'^\d{4}$', linea_limpia):
            continue

        # Si la línea sobrevivió todas las validaciones, agregarla
        if linea_limpia:
            lineas_limpias.append(linea_limpia)

    # Paso 6: Unir las líneas limpias
    texto_final = '\n'.join(lineas_limpias)

    # Paso 7: Eliminar saltos de línea múltiples (por si acaso)
    texto_final = re.sub(r'\n\s*\n', '\n', texto_final)

    return texto_final.strip()

# Función adicional para casos específicos
def limpiar_texto_modelos_personalizado(texto, palabras_adicionales=None):
    """
    Versión personalizable que permite agregar palabras específicas a eliminar
    """
    if palabras_adicionales:
        # Hacer una copia de la función original pero agregando palabras personalizadas
        texto_temp = texto
        for palabra in palabras_adicionales:
            patron_palabra = r'\b' + re.escape(palabra) + r'\b'
            texto_temp = re.sub(patron_palabra, '', texto_temp, flags=re.IGNORECASE)

        # Aplicar la limpieza normal
        return limpiar_texto_modelos(texto_temp)
    else:
        return limpiar_texto_modelos(texto)