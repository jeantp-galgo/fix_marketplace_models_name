import json

def process_answer(answer):
    print(answer)
    try:
        # Limpia la respuesta de marcadores de código y espacios extra
        respuesta_limpia = answer['respuesta'].replace('```json', '').replace('```', '').strip()
        answer_json = json.loads(respuesta_limpia)
        return answer_json
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return answer