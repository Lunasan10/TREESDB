import json, random

random.seed(42)

nombres = ["Ana","Luis","María","Pedro","Sofía","Carlos","Laura","Jorge",
           "Isabel","Andrés","Valentina","Diego","Camila","Sebastián",
           "Daniela","Felipe","Natalia","Alejandro","Paola","Ricardo"]
apellidos = ["García","Martínez","López","Sánchez","Torres","Ruiz","Díaz",
             "Vargas","Mora","Castro","Herrera","Jiménez","Romero","Álvarez",
             "Moreno","Muñoz","Alonso","Gutiérrez","Navarro","Ramos"]
ciudades = ["Bogotá","Medellín","Cali","Barranquilla","Bucaramanga",
            "Cartagena","Cúcuta","Pereira","Manizales","Santa Marta"]
departamentos = ["Sistemas","Ventas","RRHH","Finanzas","Marketing",
                 "Operaciones","TI","Legal","Logística","Dirección"]

registros = {}
for i in range(1, 101):
    registros[str(i)] = {
        "id":           i,
        "nombre":       f"{random.choice(nombres)} {random.choice(apellidos)}",
        "edad":         random.randint(18, 65),
        "ciudad":       random.choice(ciudades),
        "departamento": random.choice(departamentos),
        "salario":      round(random.uniform(1500000, 8000000), 2),
        "activo":       random.choice([True, False])
    }

estado = {
    "tablas": {
        "default": {
            "registros":    registros,
            "indices":      {},
            "siguiente_id": 101,
            "esquema":      {}
        }
    },
    "tabla_activa": "default"
}

with open("datasets/mediano.json", "w", encoding="utf-8") as f:
    json.dump(estado, f, ensure_ascii=False, indent=2)

print(f"✅ mediano.json generado con {len(registros)} registros")