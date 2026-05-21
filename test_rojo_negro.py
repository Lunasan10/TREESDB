from estructuras.rojo_negro import RojoNegro

rn = RojoNegro()
for val in [30, 10, 50, 5, 20, 40, 60]:
    rn.insertar(val)

rn._imprimir_arbol()
print("En orden:", rn.en_orden())
print("Raíz es negra:", not rn._es_rojo(rn.raiz))