from openai_utils.templates.gpt_questions import obtener_respuesta
from openai_utils.utils.processing_answer import process_answer
from openai_utils.templates.motorcycles_type.types import get_motorcycles_types

def get_marketplace_descriptions(brand, model):

    # Modificación del prompt para obtener una respuesta estructurada
    pregunta = f"""
    Necesito una descripción para marketplace con un mínimo de 500 caracteres y un máximo de 700 caracteres y una descripción SEO con un máximo de 300 caracteres. Es importante que no incluyas el año del modelo en la descripción. El producto es el siguiente: {brand} {model}.
    Por favor, responde en el siguiente formato JSON:
    {{
        "Descripcion Marketplace": "Aquí va la descripción para el marketplace.",
        "Descripcion SEO": "Aquí va la descripción SEO."
    }}
    """
    # Ya que el prompt es largo, se le agrega un límite de tokens
    respuesta = obtener_respuesta(pregunta, 1100)
    gpt_answer = process_answer(respuesta)
    return gpt_answer