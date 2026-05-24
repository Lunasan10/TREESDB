from storage_manager import StorageManager

sm = StorageManager()

# insertar registros
sm.insert({"nombre": "Ana",   "edad": 25, "ciudad": "Bogotá"})
sm.insert({"nombre": "Luis",  "edad": 30, "ciudad": "Medellín"})
sm.insert({"nombre": "María", "edad": 22, "ciudad": "Bogotá"})
sm.insert({"nombre": "Pedro", "edad": 28, "ciudad": "Cali"})
sm.insert({"nombre": "Sofía", "edad": 22, "ciudad": "Bogotá"})

print("── SELECT id = 3")
print(sm.select("id", 3))

print("\n── SELECT nombre = Ana")
print(sm.select("nombre", "Ana"))

print("\n── RANGE edad 22 28")
print(sm.range("edad", 22, 28))

print("\n── INDEX ciudad")
print(sm.index("ciudad"))

print("\n── SELECT ciudad = Bogotá (con índice)")
print(sm.select("ciudad", "Bogotá"))

print("\n── DELETE nombre = Luis")
print(sm.delete("nombre", "Luis"), "registro(s) eliminado(s)")

print("\n── SELECT id = 2 (debe estar vacío)")
print(sm.select("id", 2))

print("\n── INFO")
print(sm.info())