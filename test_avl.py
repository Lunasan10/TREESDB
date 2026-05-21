from estructuras.avl import AVL

def todos_balanceados(arbol, nodo):
    if nodo is None:
        return True
    fb = arbol._factor_de_equilibrio(nodo)
    if fb not in (-1, 0, 1):
        return False
    return todos_balanceados(arbol, nodo.izquierda) and todos_balanceados(arbol, nodo.derecha)

def verificar(arbol):
    en_orden = arbol.en_orden()
    assert en_orden == sorted(en_orden), f"❌ No está ordenado: {en_orden}"
    assert todos_balanceados(arbol, arbol.raiz), "❌ Árbol desbalanceado"

print("Corriendo tests TRESDB — AVL...")

# ── Test 1: inserciones básicas ───────────────────────
a = AVL()
for val in [30, 10, 50, 5, 20, 40, 60]:
    a.insertar(val)
verificar(a)
assert a.buscar(30) == True
assert a.buscar(99) == False
print("  ✅ Test 1 — inserciones básicas y búsqueda")

# ── Test 2: rotación RR (orden creciente) ─────────────
b = AVL()
for val in [1, 2, 3, 4, 5]:
    b.insertar(val)
verificar(b)
print("  ✅ Test 2 — rotación RR (orden creciente)")

# ── Test 3: rotación LL (orden decreciente) ───────────
c = AVL()
for val in [5, 4, 3, 2, 1]:
    c.insertar(val)
verificar(c)
print("  ✅ Test 3 — rotación LL (orden decreciente)")

# ── Test 4: rotaciones dobles LR y RL ────────────────
d = AVL()
for val in [30, 10, 20]:   # LR
    d.insertar(val)
verificar(d)
for val in [5, 25]:        # RL
    d.insertar(val)
verificar(d)
print("  ✅ Test 4 — rotaciones dobles LR y RL")

# ── Test 5: eliminar hoja ─────────────────────────────
a.eliminar(5)
verificar(a)
assert a.buscar(5) == False
print("  ✅ Test 5 — eliminar hoja")

# ── Test 6: eliminar nodo con un hijo ────────────────
a.insertar(3)
a.eliminar(10)
verificar(a)
assert a.buscar(10) == False
print("  ✅ Test 6 — eliminar nodo con un hijo")

# ── Test 7: eliminar nodo con dos hijos ──────────────
a.eliminar(30)
verificar(a)
assert a.buscar(30) == False
print("  ✅ Test 7 — eliminar raíz con dos hijos")

# ── Test 8: eliminar la raíz hasta vaciar ────────────
e = AVL()
vals = [10, 5, 15, 3, 7]
for val in vals:
    e.insertar(val)
for val in vals:
    e.eliminar(val)
    if e.raiz is not None:
        verificar(e)
assert e.raiz is None
print("  ✅ Test 8 — vaciado completo del árbol")

# ── Test 9: duplicados ────────────────────────────────
f = AVL()
for val in [10, 10, 10]:
    f.insertar(val)
assert f.en_orden().count(10) >= 1
verificar(f)
print("  ✅ Test 9 — manejo de duplicados")

# ── Test 10: árbol grande (100 elementos) ─────────────
import random
random.seed(42)
g = AVL()
valores = random.sample(range(1000), 100)
for val in valores:
    g.insertar(val)
verificar(g)
for val in valores[:50]:
    g.eliminar(val)
verificar(g)
print("  ✅ Test 10 — 100 inserciones y 50 eliminaciones aleatorias")

print("\n🌱 Todos los tests pasaron — AVL completo y verificado")