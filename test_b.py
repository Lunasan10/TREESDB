from estructuras.arbol_b import ArbolB

b = ArbolB(t=2)
for val in [10, 20, 30, 40, 50, 60, 70]:
    b.insertar(val)

b._imprimir_arbol()
print("En orden:", b.en_orden())
print("¿Ordenado?", b.en_orden() == sorted(b.en_orden()))
print("buscar(30):", b.buscar(30))
print("buscar(99):", b.buscar(99))