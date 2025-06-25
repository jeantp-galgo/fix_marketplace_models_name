from openai import OpenAI # Conectarse al cliente de OpenAI y usar GPT

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
                {"role": "system", "content": "Eres un asistente que sabe de motos y autos."},
                {"role": "user", "content": pregunta}
            ],
            max_tokens=tokens  # Ajusta el número de tokens según tus necesidades
        )

        respuesta = response.choices[0].message.content
        return {"respuesta": respuesta}
    except Exception as e:
        return {"error": f"Error al obtener respuesta: {e}"}