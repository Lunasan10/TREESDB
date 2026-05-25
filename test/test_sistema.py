import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from query_engine import QueryEngine

qe = QueryEngine()

print("Corriendo tests de sistema TRESDB...")

# ── Test 1: INSERT básico ─────────────────────────────
r = qe.ejecutar("INSERT nombre:Ana edad:25 ciudad:Bogotá")
assert r["tipo"] == "insert", "❌ INSERT falló"
assert r["datos"][0]["nombre"] == "Ana"
assert r["datos"][0]["id"] == 1
print("  ✅ Test 1 — INSERT básico")

# ── Test 2: INSERT múltiples ──────────────────────────
for cmd in [
    "INSERT nombre:Luis  edad:30 ciudad:Medellín",
    "INSERT nombre:María edad:22 ciudad:Bogotá",
    "INSERT nombre:Pedro edad:28 ciudad:Cali",
    "INSERT nombre:Sofía edad:22 ciudad:Bogotá",
]:
    r = qe.ejecutar(cmd)
    assert r["tipo"] == "insert"
print("  ✅ Test 2 — INSERT múltiples")

# ── Test 3: SELECT por id ─────────────────────────────
r = qe.ejecutar("SELECT id = 1")
assert len(r["datos"]) == 1
assert r["datos"][0]["nombre"] == "Ana"
assert r["arbol"] == "AVL"
print("  ✅ Test 3 — SELECT por id (AVL)")

# ── Test 4: SELECT por campo sin índice ───────────────
r = qe.ejecutar("SELECT nombre = Luis")
assert len(r["datos"]) == 1
assert r["datos"][0]["edad"] == 30
assert r["arbol"] == "B+"
print("  ✅ Test 4 — SELECT por campo sin índice (B+)")

# ── Test 5: RANGE ─────────────────────────────────────
r = qe.ejecutar("RANGE edad 22 28")
assert len(r["datos"]) == 4
assert r["arbol"] == "B+"
print("  ✅ Test 5 — RANGE (B+)")

# ── Test 6: INDEX ─────────────────────────────────────
r = qe.ejecutar("INDEX ciudad")
assert r["tipo"] == "index"
assert r["arbol"] == "Rojo-Negro"
print("  ✅ Test 6 — INDEX (Rojo-Negro)")

# ── Test 7: SELECT con índice secundario ──────────────
r = qe.ejecutar("SELECT ciudad = Bogotá")
assert len(r["datos"]) == 3
assert r["arbol"] == "Rojo-Negro"
print("  ✅ Test 7 — SELECT con índice (Rojo-Negro)")

# ── Test 8: DELETE ────────────────────────────────────
r = qe.ejecutar("DELETE nombre = Luis")
assert "1 registro(s)" in r["mensaje"]
r = qe.ejecutar("SELECT id = 2")
assert len(r["datos"]) == 0
print("  ✅ Test 8 — DELETE")

# ── Test 9: RANGE después de DELETE ───────────────────
r = qe.ejecutar("RANGE edad 22 30")
edades = [d["edad"] for d in r["datos"]]
assert 30 not in edades   # Luis fue eliminado
print("  ✅ Test 9 — RANGE después de DELETE")

# ── Test 10: INFO ─────────────────────────────────────
r = qe.ejecutar("INFO")
assert r["datos"][0]["registros"] == 4
assert "ciudad" in r["datos"][0]["indices"]
print("  ✅ Test 10 — INFO")

# ── Test 11: SAVE/LOAD persistencia ───────────────────
import tempfile

with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
    ruta = tmp.name

r = qe.ejecutar(f"SAVE {ruta}")
assert r["tipo"] == "save"
assert "Estado guardado" in r["mensaje"]

qe2 = QueryEngine()
r2 = qe2.ejecutar(f"LOAD {ruta}")
assert r2["tipo"] == "load"
assert "Estado cargado" in r2["mensaje"]
assert qe2.ejecutar("INFO")["datos"][0]["registros"] == 4

import os
os.remove(ruta)
print("  ✅ Test 11 — SAVE/LOAD persistencia")

# ── Test 12: HELP ─────────────────────────────────────
r = qe.ejecutar("HELP")
assert r["tipo"] == "help"
assert len(r["mensaje"]) > 0
r = qe.ejecutar("HELP INSERT")
assert "INSERT" in r["mensaje"]
print("  ✅ Test 12 — HELP")

# ── Test 12: comandos inválidos ───────────────────────
r = qe.ejecutar("INSERTAR algo")
assert "error" in r
r = qe.ejecutar("SELECT sinigual")
assert "error" in r
r = qe.ejecutar("")
assert "error" in r
print("  ✅ Test 12 — comandos inválidos")

# ── Test 13: DELETE total y reinserción ───────────────
qe2 = QueryEngine()
for i in range(5):
    qe2.ejecutar(f"INSERT clave:val{i}")
for i in range(1, 6):
    qe2.ejecutar(f"DELETE id = {i}")
r = qe2.ejecutar("INSERT nombre:nuevo edad:1")
assert r["tipo"] == "insert"
print("  ✅ Test 13 — DELETE total y reinserción")

# ── Test 14: USE TREE ─────────────────────────────────
r = qe.ejecutar("USE TREE avl")
assert r["tipo"] == "use_tree"
assert r["arbol"] == "avl"
r = qe.ejecutar("USE TREE auto")
assert r["arbol"] == "auto"
print("  ✅ Test 14 — USE TREE")

# ── Test 15: INSERT masivo 100 registros ──────────────
qe3 = QueryEngine()
for i in range(100):
    r = qe3.ejecutar(f"INSERT id_externo:{i} valor:{i*2} grupo:{i%5}")
    assert r["tipo"] == "insert"
r = qe3.ejecutar("RANGE valor 0 50")
assert len(r["datos"]) == 26   # 0,2,4,...,50
r = qe3.ejecutar("INDEX grupo")
assert r["tipo"] == "index"
r = qe3.ejecutar("SELECT grupo = 0")
assert len(r["datos"]) == 20   # 100/5
print("  ✅ Test 15 — INSERT masivo 100 registros + INDEX + SELECT")

print("\n🌱 Todos los tests de sistema pasaron — TRESDB listo para demo")