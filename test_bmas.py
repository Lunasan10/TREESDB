# test_bmas.py
from estructuras.arbol_bmas import ArbolBMas
import random

def verificar(arbol):
    # 1. en orden correcto
    en_orden = arbol.en_orden()
    assert en_orden == sorted(en_orden), f"❌ No está ordenado: {en_orden}"

    # 2. hojas enlazadas == en_orden
    hojas = []
    hoja = arbol.primera_hoja
    while hoja is not None:
        hojas.extend(hoja.claves)
        hoja = hoja.siguiente
    assert hojas == en_orden, f"❌ Hojas desincronizadas: {hojas} vs {en_orden}"

    # 3. estructura del árbol válida
    if arbol.raiz and len(arbol.raiz.claves) > 0:
        _verificar_nodo(arbol, arbol.raiz, es_raiz=True)

def _verificar_nodo(arbol, nodo, es_raiz=False):
    t = arbol.t
    max_claves = 2 * t - 1
    min_claves = 1 if es_raiz else t - 1
    assert len(nodo.claves) <= max_claves, f"❌ Demasiadas claves: {nodo.claves}"
    assert len(nodo.claves) >= min_claves, f"❌ Pocas claves: {nodo.claves}"
    if not nodo.hoja:
        assert len(nodo.hijos) == len(nodo.claves) + 1, f"❌ Hijos incorrectos: {nodo.claves}"
        for hijo in nodo.hijos:
            _verificar_nodo(arbol, hijo, es_raiz=False)

print("Corriendo tests TRESDB — Árbol B+...")

# ── Test 1: inserciones básicas ───────────────────────
a = ArbolBMas(t=2)
for val in [10, 20, 30, 40, 50, 60, 70]:
    a.insertar(val)
verificar(a)
assert a.buscar(30) == True
assert a.buscar(99) == False
print("  ✅ Test 1 — inserciones básicas y búsqueda")

# ── Test 2: hojas enlazadas correctas ────────────────
assert a.rango(20, 50) == [20, 30, 40, 50]
assert a.rango(1, 100) == [10, 20, 30, 40, 50, 60, 70]
assert a.rango(35, 55) == [40, 50]
assert a.rango(100, 200) == []
print("  ✅ Test 2 — RANGE correcto")

# ── Test 3: inserción orden creciente ────────────────
b = ArbolBMas(t=2)
for val in [1, 2, 3, 4, 5, 6, 7, 8]:
    b.insertar(val)
verificar(b)
assert b.rango(3, 6) == [3, 4, 5, 6]
print("  ✅ Test 3 — inserción orden creciente")

# ── Test 4: inserción orden decreciente ──────────────
c = ArbolBMas(t=2)
for val in [8, 7, 6, 5, 4, 3, 2, 1]:
    c.insertar(val)
verificar(c)
assert c.rango(2, 5) == [2, 3, 4, 5]
print("  ✅ Test 4 — inserción orden decreciente")

# ── Test 5: eliminar clave en nodo interno ────────────
a.eliminar(30)
verificar(a)
assert a.buscar(30) == False
assert a.rango(20, 50) == [20, 40, 50]
print("  ✅ Test 5 — eliminar clave en nodo interno")

# ── Test 6: eliminar hoja ────────────────────────────
a.eliminar(10)
verificar(a)
assert a.buscar(10) == False
print("  ✅ Test 6 — eliminar hoja")

# ── Test 7: eliminar hasta vaciar ────────────────────
d = ArbolBMas(t=2)
vals = [10, 20, 30, 40, 50]
for val in vals:
    d.insertar(val)
for val in vals:
    d.eliminar(val)
    if d.raiz and len(d.raiz.claves) > 0:
        verificar(d)
assert d.en_orden() == []
print("  ✅ Test 7 — vaciado completo")

# ── Test 8: RANGE en límites exactos ─────────────────
e = ArbolBMas(t=2)
for val in [10, 20, 30, 40, 50]:
    e.insertar(val)
assert e.rango(10, 10) == [10]
assert e.rango(50, 50) == [50]
assert e.rango(10, 50) == [10, 20, 30, 40, 50]
print("  ✅ Test 8 — RANGE en límites exactos")

# ── Test 9: t=3 con muchos elementos ─────────────────
f = ArbolBMas(t=3)
for val in range(1, 30):
    f.insertar(val)
verificar(f)
assert f.rango(5, 15) == list(range(5, 16))
print("  ✅ Test 9 — t=3 con 29 elementos")

# ── Test 10: 100 elementos aleatorios ────────────────
random.seed(42)
g = ArbolBMas(t=3)
valores = random.sample(range(1000), 100)
for val in valores:
    g.insertar(val)
verificar(g)
for val in valores[:50]:
    g.eliminar(val)
verificar(g)
print("  ✅ Test 10 — 100 inserciones y 50 eliminaciones aleatorias")

print("\n🌱 Todos los tests pasaron — Árbol B+ completo y verificado")