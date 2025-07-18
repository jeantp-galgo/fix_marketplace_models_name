import re

def get_modelos_from_text(texto_modelos_desordenados: str, nombre_marca: str) -> list[str]:
    # Convertir el texto de marca a una lista de modelos
    modelos_marca = texto_modelos_desordenados.split('\n')

    # Filtrar elementos vacíos y limpiar la lista
    modelos_limpios = [modelo.strip() for modelo in modelos_marca if modelo.strip()]

    # Filtrar años que empiecen por 2000 (4 dígitos) y eliminar años del texto
    import re
    modelos_sin_anos = []
    for modelo in modelos_limpios:
        # Eliminar años de 4 dígitos que empiecen con 20
        modelo_limpio = re.sub(r'\b20\d{2}\b', '', modelo).strip()
        # Solo agregar si no es solo un año de 4 dígitos
        if not (len(modelo) == 4 and modelo.startswith('20')):
            if modelo_limpio:  # Solo agregar si no queda vacío después de limpiar
                # Eliminar guiones al inicio y espacios extra
                modelo_final = re.sub(r'^-\s*', '', modelo_limpio).strip()
                if modelo_final:  # Solo agregar si no queda vacío después de limpiar
                    # Verificar si el modelo ya contiene el nombre de la marca
                    if nombre_marca.upper() not in modelo_final.upper():
                        # Agregar el nombre de la marca al inicio si no lo tiene
                        modelo_con_marca = f"{nombre_marca} {modelo_final}"
                        modelos_sin_anos.append(modelo_con_marca)
                    else:
                        # Si ya tiene el nombre de la marca, agregarlo tal como está
                        modelos_sin_anos.append(modelo_final)

    # Primero agregar la marca a todos los modelos que no la tengan
    modelos_con_marca = []
    for modelo in modelos_sin_anos:
        if nombre_marca.upper() not in modelo.upper():
            modelo_con_marca = f"{nombre_marca} {modelo}"
            modelos_con_marca.append(modelo_con_marca)
        else:
            modelos_con_marca.append(modelo)

    # Función para limpiar el modelo preservando el formato original
    def limpiar_modelo(texto: str) -> str:
        # Solo hacer limpieza básica sin cambiar mayúsculas/minúsculas

        # Eliminar espacios extra
        texto = re.sub(r'\s+', ' ', texto).strip()

        # Eliminar caracteres especiales al inicio/final
        texto = re.sub(r'^[-\s]+|[-\s]+$', '', texto)

        # Corregir solo casos obvios donde la marca esté duplicada
        palabras = texto.split()
        if len(palabras) > 1 and palabras[0].upper() == palabras[1].upper() == nombre_marca.upper():
            # Remover marca duplicada
            texto = ' '.join(palabras[1:])

        return texto

    # Aplicar solo limpieza básica, preservando formato original
    modelos_limpios_final = [limpiar_modelo(modelo) for modelo in modelos_con_marca]

    # Eliminar duplicados y elementos vacíos
    modelos_finales = [modelo for modelo in list(set(modelos_limpios_final)) if modelo.strip()]

    return modelos_finales