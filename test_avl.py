from estructuras.avl import AVL

a = AVL()
for val in [30, 10, 50, 5, 20, 40, 60]:
    a.insertar(val)
    
print(a.en_orden())
print(a.buscar(20))
print(a.buscar(99))
print(a.raiz.clave)
print(a.raiz.altura)
a._imprimir_arbol()

print("____________________________________")

b = AVL()
for val in [10, 20, 30, 40, 50, 60, 7, 5, 3]:
    b.insertar(val)

b._imprimir_arbol()