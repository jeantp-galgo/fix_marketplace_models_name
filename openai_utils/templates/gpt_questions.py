from openai import OpenAI # Conectarse al cliente de OpenAI y usar GPT
from difflib import get_close_matches
import re

from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
)

def obtener_respuesta(pregunta, tokens=150):
    try:
        # Realiza la solicitud a la API de OpenAI utilizando la nueva interfaz
        response = client.chat.completions.create(

            model="gpt-3.5-turbo",  # Asegúrate de usar el modelo correcto
            messages=[
                {"role": "system", "content": "Eres un asistente que identificar nombres de modelos de motos correctos"},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=tokens  # Ajusta el número de tokens según tus necesidades
        )

        respuesta = response.choices[0].message.content
        return {"respuesta": respuesta}
    except Exception as e:
        return {"error": f"Error al obtener respuesta: {e}"}

def obtener_respuesta_correcto(pregunta, tokens=150):
    try:
        # Realiza la solicitud a la API de OpenAI utilizando la nueva interfaz
        response = client.chat.completions.create(

            model="gpt-4o-mini",  # Modelo mejorado para mejor precisión
            # model="gpt-4",  # Modelo mejorado para mejor precisión
            messages=[
                {"role": "system", "content": "Eres un experto en motocicletas especializado en identificar y corregir nombres de modelos de motos. Tu tarea es encontrar el nombre correcto del modelo basándote en la información proporcionada. Debes ser preciso y considerar variaciones comunes en la escritura de modelos (espacios, guiones, mayúsculas, etc.)."},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=tokens  # Ajusta el número de tokens según tus necesidades
        )

        respuesta = response.choices[0].message.content
        return {"respuesta": respuesta}
    except Exception as e:
        return {"error": f"Error al obtener respuesta: {e}"}

def normalizar_modelo(modelo):
    """Normaliza el nombre del modelo para comparaciones"""
    # Convertir a minúsculas y quitar espacios extra
    modelo = re.sub(r'\s+', ' ', modelo.lower().strip())
    # Quitar caracteres especiales comunes
    modelo = re.sub(r'[^\w\s]', '', modelo)
    return modelo

def buscar_coincidencia_exacta(nombre_incorrecto, catalogo_modelos):
    """Busca coincidencia exacta primero"""
    nombre_norm = normalizar_modelo(nombre_incorrecto)

    for modelo in catalogo_modelos:
        if normalizar_modelo(modelo) == nombre_norm:
            return modelo
    return None

def buscar_coincidencia_algoritmica(nombre_incorrecto, catalogo_modelos, umbral=0.8):
    """Busca coincidencias usando algoritmos de similitud"""
    nombre_norm = normalizar_modelo(nombre_incorrecto)
    catalogo_norm = [normalizar_modelo(m) for m in catalogo_modelos]

    # Usar difflib para encontrar coincidencias cercanas
    coincidencias = get_close_matches(nombre_norm, catalogo_norm, n=3, cutoff=umbral)

    if coincidencias:
        # Devolver el modelo original correspondiente a la mejor coincidencia
        indice = catalogo_norm.index(coincidencias[0])
        return catalogo_modelos[indice]

    return None

def homologar_modelo_hibrido(nombre_incorrecto, catalogo_modelos, marca="", usar_ia=True):
    """
    Función híbrida que combina algoritmos de búsqueda con IA
    """
    # Paso 1: Buscar coincidencia exacta
    coincidencia_exacta = buscar_coincidencia_exacta(nombre_incorrecto, catalogo_modelos)
    if coincidencia_exacta:
        return {"respuesta": coincidencia_exacta, "metodo": "exacta"}

    # Paso 2: Buscar coincidencia algorítmica
    coincidencia_algoritmica = buscar_coincidencia_algoritmica(nombre_incorrecto, catalogo_modelos)
    if coincidencia_algoritmica:
        return {"respuesta": coincidencia_algoritmica, "metodo": "algoritmica"}

    # Paso 3: Si no hay coincidencias algorítmicas y se permite IA, usar IA
    if usar_ia:
        resultado_ia = homologar_modelo_con_catalogo(nombre_incorrecto, catalogo_modelos, marca)
        if resultado_ia.get("respuesta") and resultado_ia["respuesta"] != "No encontrado":
            return {"respuesta": resultado_ia["respuesta"], "metodo": "ia"}

    return {"respuesta": "No encontrado", "metodo": "ninguno"}

def homologar_modelo_con_catalogo(nombre_incorrecto, catalogo_modelos, marca="", tokens=200):
    """
    Función especializada para homologar nombres de modelos usando el catálogo completo
    """
    try:
        # Crear el prompt con el catálogo completo
        catalogo_texto = "\n".join([f"- {modelo}" for modelo in catalogo_modelos])

        prompt = f"""
TAREA: Encuentra el modelo EXACTO del catálogo que corresponde al nombre proporcionado.

NOMBRE A CORREGIR: "{nombre_incorrecto}"
MARCA: {marca if marca else "No especificada"}

CATÁLOGO COMPLETO DE MODELOS DISPONIBLES:
{catalogo_texto}

INSTRUCCIONES CRÍTICAS:
1. SOLO puedes elegir un modelo que esté EXACTAMENTE en el catálogo anterior
2. Busca coincidencias considerando:
   - Números pueden estar separados o juntos (150XC vs 150 XC)
   - Letras pueden variar (XC vs EXC, S vs R)
   - Espacios y guiones pueden variar
   - Mayúsculas/minúsculas pueden diferir
3. Si encuentras el modelo EXACTO en el catálogo, devuélvelo tal como aparece
4. Si no encuentras coincidencia exacta, busca el más similar
5. Solo responde "No encontrado" si realmente no hay ninguna coincidencia razonable

FORMATO DE RESPUESTA: Solo el nombre del modelo del catálogo, nada más.

EJEMPLOS:
- Si buscas "1290 Super Adventure S" y está en el catálogo, responde: "1290 Super Adventure S"
- Si buscas "150 XC" y el catálogo tiene "150 EXC", responde: "150 EXC"
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en identificación exacta de modelos de motocicletas. Tu única tarea es encontrar coincidencias exactas en el catálogo proporcionado."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=tokens,
            temperature=0.1  # Temperatura baja para respuestas más deterministas
        )

        respuesta = response.choices[0].message.content.strip()
        return {"respuesta": respuesta}
    except Exception as e:
        return {"error": f"Error al obtener respuesta: {e}"}