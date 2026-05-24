# test_rojo_negro.py

from estructuras.rojo_negro import RojoNegro

def contar_negros_camino(arbol, nodo):
    if nodo is None:
        return 1
    izq = contar_negros_camino(arbol, nodo.izquierda)
    der = contar_negros_camino(arbol, nodo.derecha)
    if izq == -1 or der == -1:
        return -1
    if izq != der:
        return -1
    return izq + (1 if not arbol._es_rojo(nodo) else 0)

def verificar(arbol):
    en_orden = arbol.en_orden()
    assert en_orden == sorted(en_orden), f"❌ No está ordenado: {en_orden}"
    assert not arbol._es_rojo(arbol.raiz), "❌ La raíz debe ser negra"

    def sin_rojos_consecutivos(nodo):
        if nodo is None:
            return True
        if arbol._es_rojo(nodo):
            assert not arbol._es_rojo(nodo.izquierda), f"❌ Rojo consecutivo en {nodo.clave}"
            assert not arbol._es_rojo(nodo.derecha),   f"❌ Rojo consecutivo en {nodo.clave}"
        return sin_rojos_consecutivos(nodo.izquierda) and sin_rojos_consecutivos(nodo.derecha)

    sin_rojos_consecutivos(arbol.raiz)
    assert contar_negros_camino(arbol, arbol.raiz) != -1, "❌ Negros desiguales por camino"

print("Corriendo tests TRESDB — Rojo-Negro...")

# ── Test 1: inserciones básicas ───────────────────────
a = RojoNegro()
for val in [30, 10, 50, 5, 20, 40, 60]:
    a.insertar(val)
verificar(a)
assert a.buscar(30) == True
assert a.buscar(99) == False
print("  ✅ Test 1 — inserciones básicas y búsqueda")

# ── Test 2: inserción en orden creciente ──────────────
b = RojoNegro()
for val in [1, 2, 3, 4, 5]:
    b.insertar(val)
verificar(b)
print("  ✅ Test 2 — inserción orden creciente")

# ── Test 3: inserción en orden decreciente ────────────
c = RojoNegro()
for val in [5, 4, 3, 2, 1]:
    c.insertar(val)
verificar(c)
print("  ✅ Test 3 — inserción orden decreciente")

# ── Test 4: eliminar hoja roja ────────────────────────
a.eliminar(5)
verificar(a)
assert a.buscar(5) == False
print("  ✅ Test 4 — eliminar hoja roja")

# ── Test 5: eliminar hoja negra ───────────────────────
a.eliminar(20)
verificar(a)
assert a.buscar(20) == False
print("  ✅ Test 5 — eliminar hoja negra")

# ── Test 6: eliminar nodo con un hijo ────────────────
a.eliminar(10)
verificar(a)
assert a.buscar(10) == False
print("  ✅ Test 6 — eliminar nodo con un hijo")

# ── Test 7: eliminar nodo con dos hijos ──────────────
a.eliminar(30)
verificar(a)
assert a.buscar(30) == False
print("  ✅ Test 7 — eliminar nodo con dos hijos")

# ── Test 8: eliminar la raíz ─────────────────────────
d = RojoNegro()
for val in [10, 5, 15]:
    d.insertar(val)
d.eliminar(10)
verificar(d)
assert d.buscar(10) == False
print("  ✅ Test 8 — eliminar la raíz")

# ── Test 9: vaciado completo ──────────────────────────
e = RojoNegro()
vals = [10, 5, 15, 3, 7]
for val in vals:
    e.insertar(val)
for val in vals:
    e.eliminar(val)
    if e.raiz is not None:
        verificar(e)
assert e.raiz is None
print("  ✅ Test 9 — vaciado completo")

# ── Test 10: 100 elementos aleatorios ────────────────
import random
random.seed(42)
f = RojoNegro()
valores = random.sample(range(1000), 100)
for val in valores:
    f.insertar(val)
verificar(f)
for val in valores[:50]:
    f.eliminar(val)
    verificar(f)
print("  ✅ Test 10 — 100 inserciones y 50 eliminaciones aleatorias")

print("\n🌱 Todos los tests pasaron — Rojo-Negro completo y verificado")