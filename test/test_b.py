# test_b.py
from estructuras.arbol_b import ArbolB

def verificar(arbol):
    en_orden = arbol.en_orden()
    assert en_orden == sorted(en_orden), f"❌ No está ordenado: {en_orden}"
    assert len(en_orden) == len(set(en_orden)), "❌ Hay duplicados"
    _verificar_nodo(arbol, arbol.raiz, es_raiz=True)

def _verificar_nodo(arbol, nodo, es_raiz=False):
    t = arbol.t
    max_claves = 2 * t - 1
    min_claves = 1 if es_raiz else t - 1

    assert len(nodo.claves) <= max_claves, f"❌ Nodo con demasiadas claves: {nodo.claves}"
    assert len(nodo.claves) >= min_claves, f"❌ Nodo con pocas claves: {nodo.claves}"

    if not nodo.hoja:
        assert len(nodo.hijos) == len(nodo.claves) + 1, f"❌ Hijos incorrectos en: {nodo.claves}"
        for hijo in nodo.hijos:
            _verificar_nodo(arbol, hijo, es_raiz=False)

print("Corriendo tests TRESDB — Árbol B...")

# ── Test 1: inserciones básicas ───────────────────────
a = ArbolB(t=2)
for val in [10, 20, 30, 40, 50, 60, 70]:
    a.insertar(val)
verificar(a)
assert a.buscar(30) == True
assert a.buscar(99) == False
print("  ✅ Test 1 — inserciones básicas y búsqueda")

# ── Test 2: inserción en orden creciente ──────────────
b = ArbolB(t=2)
for val in [1, 2, 3, 4, 5, 6, 7, 8]:
    b.insertar(val)
verificar(b)
print("  ✅ Test 2 — inserción orden creciente")

# ── Test 3: inserción en orden decreciente ────────────
c = ArbolB(t=2)
for val in [8, 7, 6, 5, 4, 3, 2, 1]:
    c.insertar(val)
verificar(c)
print("  ✅ Test 3 — inserción orden decreciente")

# ── Test 4: grado mínimo t=3 ─────────────────────────
d = ArbolB(t=3)
for val in range(1, 20):
    d.insertar(val)
verificar(d)
print("  ✅ Test 4 — grado mínimo t=3")

# ── Test 5: eliminar hoja ────────────────────────────
a.eliminar(10)
verificar(a)
assert a.buscar(10) == False
print("  ✅ Test 5 — eliminar hoja")

# ── Test 6: eliminar nodo interno ────────────────────
a.eliminar(20)
verificar(a)
assert a.buscar(20) == False
print("  ✅ Test 6 — eliminar nodo interno")

# ── Test 7: eliminar la raíz ─────────────────────────
a.eliminar(40)
verificar(a)
assert a.buscar(40) == False
print("  ✅ Test 7 — eliminar la raíz")

# ── Test 8: vaciado completo ─────────────────────────
e = ArbolB(t=2)
vals = [10, 20, 30, 40, 50]
for val in vals:
    e.insertar(val)
for val in vals:
    e.eliminar(val)
assert e.raiz is not None
assert len(e.raiz.claves) == 0
print("  ✅ Test 8 — vaciado completo")

# ── Test 9: eliminar clave inexistente ───────────────
f = ArbolB(t=2)
for val in [10, 20, 30]:
    f.insertar(val)
f.eliminar(99)
verificar(f)
assert f.en_orden() == [10, 20, 30]
print("  ✅ Test 9 — eliminar clave inexistente")

# ── Test 10: 100 elementos aleatorios ────────────────
import random
random.seed(42)
g = ArbolB(t=3)
valores = random.sample(range(1000), 100)
for val in valores:
    g.insertar(val)
verificar(g)
for val in valores[:50]:
    g.eliminar(val)
verificar(g)
print("  ✅ Test 10 — 100 inserciones y 50 eliminaciones aleatorias")

print("\n🌱 Todos los tests pasaron — Árbol B completo y verificado")