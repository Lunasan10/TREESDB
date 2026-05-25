from storage_manager import StorageManager

sm = StorageManager()

# insertar registros
r1 = sm.insert({"nombre": "Ana",   "edad": 25, "ciudad": "Bogotá"})
r2 = sm.insert({"nombre": "Luis",  "edad": 30, "ciudad": "Medellín"})
r3 = sm.insert({"nombre": "María", "edad": 22, "ciudad": "Bogotá"})
r4 = sm.insert({"nombre": "Pedro", "edad": 28, "ciudad": "Cali"})
r5 = sm.insert({"nombre": "Sofía", "edad": 22, "ciudad": "Bogotá"})

assert r1["id"] == 1 and r2["id"] == 2 and r3["id"] == 3 and r4["id"] == 4 and r5["id"] == 5

print("── SELECT id = 3")
sel_id_3 = sm.select("id", 3)
assert len(sel_id_3) == 1 and sel_id_3[0]["nombre"] == "María"
print(sel_id_3)

print("\n── SELECT nombre = Ana")
sel_ana = sm.select("nombre", "Ana")
assert len(sel_ana) == 1 and sel_ana[0]["edad"] == 25 
print(sel_ana)


print("\n── RANGE edad 22 28")
rango = sm.range("edad", 22, 28)
assert len(rango) == 4
assert {r["nombre"] for r in rango} == {"Ana", "María", "Pedro", "Sofía"}
print(rango)

print("\n── INDEX ciudad")
msg = sm.index("ciudad")
assert "Índice 'ciudad'" in msg
print(msg)

print("\n── SELECT ciudad = Bogotá (con índice)")
sel_bogota = sm.select("ciudad", "Bogotá")
assert len(sel_bogota) == 3
assert {r["nombre"] for r in sel_bogota} == {"Ana", "María", "Sofía"}
print(sel_bogota)

print("\n── DELETE nombre = Luis")
eliminados = sm.delete("nombre", "Luis")
assert eliminados == 1
print(eliminados, "registro(s) eliminado(s)")

print("\n── SELECT id = 2 (debe estar vacío)")
assert sm.select("id", 2) == []
print(sm.select("id", 2))

print("\n── INFO")
info = sm.info()
info = sm.info()
assert info["registros"] == 4
assert info["siguiente_id"] == 6
assert "ciudad" in info["indices"]
print(sm.info())

print("\n── UPDATE con esquema inválido")
sm_esquema = StorageManager()
sm_esquema.definir_esquema({"edad": "int"})
registro = sm_esquema.insert({"edad": 25})

try:
    sm_esquema.update("id", registro["id"], {"edad": "veinticinco"})
    assert False, "❌ UPDATE debía fallar por tipo inválido"
except TypeError:
    pass

assert sm_esquema.select("id", registro["id"])[0]["edad"] == 25
print("UPDATE rechazó el cambio inválido y conservó el registro original")