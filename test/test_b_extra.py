# test_b_extra.py
from estructuras.arbol_b import ArbolB
import random

def verificar(arbol):
    en_orden = arbol.en_orden()
    assert en_orden == sorted(en_orden), f"❌ No está ordenado: {en_orden}"
    if arbol.raiz is not None and len(arbol.raiz.claves) > 0:
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

print("Corriendo tests extra TRESDB — Árbol B...")

# ── Test 11: insertar duplicados ─────────────────────
a = ArbolB(t=2)
for val in [10, 20, 10, 30, 20]:
    a.insertar(val)
verificar(a)
en_orden = a.en_orden()
assert en_orden == sorted(en_orden), "❌ Duplicados rompieron el orden"
print(f"  ✅ Test 11 — duplicados (en orden: {en_orden})")

# ── Test 12: eliminar el mismo elemento dos veces ────
b = ArbolB(t=2)
for val in [10, 20, 30]:
    b.insertar(val)
b.eliminar(20)
b.eliminar(20)
verificar(b)
assert b.buscar(20) == False
print("  ✅ Test 12 — eliminar elemento inexistente dos veces")

# ── Test 13: árbol grande 1000 elementos ─────────────
random.seed(7)
c = ArbolB(t=3)
valores_1000 = random.sample(range(10000), 1000)
for val in valores_1000:
    c.insertar(val)
verificar(c)
assert len(c.en_orden()) == 1000
print("  ✅ Test 13 — 1000 elementos aleatorios")

# ── Test 14: árbol muy grande 10000 elementos ────────
d = ArbolB(t=4)
valores_10000 = random.sample(range(100000), 10000)
for val in valores_10000:
    d.insertar(val)
verificar(d)
assert len(d.en_orden()) == 10000
print("  ✅ Test 14 — 10000 elementos aleatorios")

# ── Test 15: inserción y eliminación intercaladas ────
e = ArbolB(t=2)
random.seed(13)
presentes = []



for ronda in range(5):
    nuevos = random.sample(range(1000), 10)
    for val in nuevos:
        e.insertar(val)
        presentes.append(val)

    print(f"Ronda {ronda} — después de insertar:")
    e._imprimir_arbol()
    verificar(e)
    

    eliminar = presentes[:5]
    
    for val in eliminar:
        e.eliminar(val)
        presentes.remove(val)
        try:
            verificar(e)
        except AssertionError as err:
            print(f"❌ Falló después de eliminar {val} en ronda {ronda}")
            e._imprimir_arbol()
            raise

print("  ✅ Test 15 — inserción y eliminación intercaladas (5 rondas)")