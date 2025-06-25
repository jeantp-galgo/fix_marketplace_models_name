tipos_motos = [
    "Scooter",
    "Naked",
    "Trail",
    "Racing",
    "Multipropósito",
    "Carga",
    "Urbana",
    "ATV",
    "Cuatrimoto",
    "Chopper",
    "Eléctrica",
    "Enduro",
    "Deportiva",
    "Todo Terreno",
    "Pistera",
    "Doble Propósito",
    "Trabajo",
    "Motoneta",
    "Carguero",
    "Lineal",
    "Touring",
    "Automática",
    "Semiautomática",
    "Trimoto",
    "Café Racer",
    "Patineta Eléctrica"
]

motorcycles_types_mx = [
    "Naked",
    "Trail",
    "Racing",
    "Carga",
    "ATV",
    "Cuatrimoto",
    "Chopper",
    "Eléctrica",
    "Enduro",
    "Deportiva",
    "Doble Propósito",
    "Trabajo",
    "Motoneta",
    "Carguero",
    "Touring",
    "Automática",
    "Semiautomática",
    "Trimoto",
    "Café Racer"
]

motorcycles_types_co = [
    "Scooter",
    "Naked",
    "Trail",
    "Racing",
    "Carga",
    "Urbana",
    "ATV",
    "Cuatrimoto",
    "Chopper",
    "Eléctrica",
    "Enduro",
    "Deportiva",
    "Todo Terreno",
    "Carguero",
    "Touring",
    "Automática",
    "Semiautomática",
    "Trimoto",
    "Café Racer",
    "Patineta Eléctrica"
]

motorcycles_types_cl = [
    "Scooter",
    "Naked",
    "Trail",
    "Racing",
    "Multipropósito",
    "Carga",
    "ATV",
    "Cuatrimoto",
    "Chopper",
    "Eléctrica",
    "Enduro",
    "Deportiva",
    "Carguero",
    "Touring",
    "Automática",
    "Semiautomática",
    "Trimoto",
    "Café Racer"
    ]


def get_motorcycles_types(country):
    if country == "MX":
        return motorcycles_types_mx
    elif country == "CO":
        return motorcycles_types_co
    elif country == "CL":
        return motorcycles_types_cl
    else:
        return tipos_motos