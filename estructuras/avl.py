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
    
    # Inserción:
    
    def insertar(self, clave):
        self.raiz = self._insertar_rec(self.raiz, clave)
    
    def _insertar_rec(self, nodo, clave):
        if nodo is None:
            return NodoAVL(clave)
        
        if clave < nodo.clave:
            nodo.izquierda = self._insertar_rec(nodo.izquierda, clave)
        else:
            nodo.derecha = self._insertar_rec(nodo.derecha, clave)
        
        return self._balancear(nodo)
    
    # Rotaciones:
    def _rotar_derecha(self, z):
        y = z.izquierda
        hijo_derecha_de_y = y.derecha
        
        # Rotación:
        y.derecha = z
        z.izquierda = hijo_derecha_de_y
        
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y
    
    def _rotar_izquierda(self, z):
        y = z.derecha
        hijo_izquierda_de_y = y.izquierda
        
        # Rotación:
        y.izquierda = z
        z.derecha = hijo_izquierda_de_y
        
        self._actualizar_altura(z)
        self._actualizar_altura(y)
        return y
    
    def _balancear(self, z):
        self._actualizar_altura(z)
        fb = self._factor_de_equilibrio(z)
        
        # LL 
        if fb == -2 and self._factor_de_equilibrio(z.izquierda) <= 0:
            return self._rotar_derecha(z)

        # LR 
        if fb == -2 and self._factor_de_equilibrio(z.izquierda) > 0:
            z.izquierda = self._rotar_izquierda(z.izquierda)
            return self._rotar_derecha(z)

        # RR 
        if fb == 2 and self._factor_de_equilibrio(z.derecha) >= 0:
            return self._rotar_izquierda(z)

        # RL
        if fb == 2 and self._factor_de_equilibrio(z.derecha) < 0:
            z.derecha = self._rotar_derecha(z.derecha)
            return self._rotar_izquierda(z)
            
        return z

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
        
    # Eliminación:
    def _minimo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    
    def eliminar(self, clave):
        self.raiz = self._eliminar_rec(self.raiz, clave)
        
    def _eliminar_rec(self, nodo, clave):
        if nodo is None:
            return None
        
        if clave < nodo.clave:
            nodo.izquierda = self._eliminar_rec(nodo.izquierda, clave)
        elif clave > nodo.clave: 
            nodo.derecha = self._eliminar_rec(nodo.derecha, clave)
        else:
            # Nodo con un solo hijo o sin hijos
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            
            # Nodo con dos hijos
            sucesor = self._minimo(nodo.derecha) # -> Menor del subárbol derecho
            nodo.clave = sucesor.clave
            nodo.derecha = self._eliminar_rec(nodo.derecha, sucesor.clave)
            
        return self._balancear(nodo)
            
    
        
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