class NodoAVL:
    def __init__(self, clave):
        self.clave = clave
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    def __init__(self):
        self.raiz = None
        
    # ALtura:
    
    def _altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura
    
    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        
    def _factor_de_equilibrio(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.derecha) - self._altura(nodo.izquierda)
    
    # Búsqueda:
    
    def buscar(self,clave):
        return self._buscar_rec(self.raiz, clave)
    
    def _buscar_rec(self, nodo, clave):
        if nodo is None:
            return False
        if clave == nodo.clave:
            return True
        if clave < nodo.clave:
            return self._buscar_rec(nodo.izquierda,clave)
        return self._buscar_rec(nodo.derecha,clave)
    
    # Inserción: (sin rotaciones aún)
    
    def insertar(self, clave):
        self.raiz = self._insertar_rec(self.raiz, clave)
    
    def _insertar_rec(self, nodo, clave):
        if nodo is None:
            return NodoAVL(clave)
        
        if clave < nodo.clave:
            nodo.izquierda = self._insertar_rec(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha = self._insertar_rec(nodo.derecha, clave)
        else:
            # Al tratarse de una Base de Datos, no se permiten claves duplicadas
            return nodo 
        
        self._actualizar_altura(nodo)
        return nodo
    
    # Recorrido:
    def en_orden(self):
        resultado = []
        self._en_orden_rec(self.raiz, resultado)
        return resultado
    
    def _en_orden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._en_orden_rec(nodo.izquierda, resultado)
        resultado.append(nodo.clave)
        self._en_orden_rec(nodo.derecha, resultado)
        
    # Imprimir:
    def _imprimir_arbol(self, nodo=None, prefijo="", es_derecha=True, primer_llamado=True):
        if primer_llamado:
            nodo = self.raiz
            if nodo is None:
                print("(Árbol vacío)")
                return
            print(f"[{nodo.clave}] fb:{self._factor_de_equilibrio(nodo)} h:{nodo.altura}")
            self._imprimir_arbol(nodo.derecha, "", True, False)
            self._imprimir_arbol(nodo.izquierda, "", False, False)
            return
        
        if nodo is None:
            return
        
        conector = "└── " if es_derecha else "├── "
        lado = "D" if es_derecha else "I"
        print(f"{prefijo}{conector}[{nodo.clave}] fb:{self._factor_de_equilibrio(nodo)} h:{nodo.altura}")
        
        extension = "    " if es_derecha else "│   "
        self._imprimir_arbol(nodo.derecha, prefijo + extension, True, False)
        self._imprimir_arbol(nodo.izquierda, prefijo + extension, False, False)