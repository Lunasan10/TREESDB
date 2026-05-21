ROJO = 0
NEGRO = 1

class NodoRN:
    def __init__(self, clave):
        self.clave = clave
        self.izquierda = None
        self.derecha = None
        self.padre = None
        self.color = ROJO

class RojoNegro:
    def __init__(self):
        self.raiz = None
    
    def _color(self, nodo):
        # Los nodos nulos/sin datos siempre son negros
        if nodo is None:
            return NEGRO
        return nodo.color
    
    def _es_rojo(self, nodo):
        return self._color(nodo) == ROJO
    
    # Insersión:
    def insertar(self, clave):
        nuevo = NodoRN(clave)
        
        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar_bts(self.raiz, nuevo)
            
        self._fix_insercion(nuevo)
        
        # La raíz siempre queda negra
        self.raiz.color = NEGRO
        
    def _insertar_bts(self, actual, nuevo):
        if nuevo.clave < actual.clave:
            if actual.izquierda is None:
                actual.izquierda = nuevo
                nuevo.padre = actual
            else:
                self._insertar_bts(actual.izquierda, nuevo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo
                nuevo.padre = actual
            else:
                self._insertar_bts(actual.derecha, nuevo)
    
    def _fix_insercion(self, nodo):
        while nodo != self.raiz and self._es_rojo(nodo.padre):
            padre = nodo.padre
            abuelo = padre.padre

            if padre == abuelo.izquierda:
                tio = abuelo.derecha
                
                # Caso 1: Tío rojo -> Recoloración de padre, tío y abuelo
                if self._es_rojo(tio):
                    padre.color = NEGRO
                    tio.color = NEGRO
                    abuelo.color = ROJO
                    nodo = abuelo
                
                else :
                    # caso 2: Tío negro y x es hijo derecho -> Rotación y verificación
                    if nodo == padre.derecha:
                        self._rotar_izquierda(padre)
                        nodo = padre
                        padre = nodo.padre
                    # caso 3: Tío negro y x es hijo izquierdo -> Rotación y recoloración
                    padre.color = NEGRO
                    abuelo.color = ROJO
                    self._rotar_derecha(abuelo)
            # Casos simétricos
            else:
                tio = abuelo.izquierda
                
                if self._es_rojo(tio):
                    padre.color = NEGRO
                    tio.color = NEGRO
                    abuelo.color = ROJO
                    nodo = abuelo
                    
                else :
                    if nodo == padre.izquierda:
                        self._rotar_derecha(padre)
                        nodo = padre
                        padre = nodo.padre
                    
                    padre.color = NEGRO
                    abuelo.color = ROJO
                    self._rotar_derecha(abuelo)
        
        self.raiz.color = NEGRO
    
    def _rotar_izquierda(self, z):
        y = z.derecha
        z.derecha = y.izquierda
        
        if y.izquierda is not None:
            y.izquierda.padre = z
        
        y.padre = z.padre
        
        if z.padre is None:
            self.raiz = y
        elif z == z.padre.izquierda:
            z.padre.izquierda = y
        else:
            z.padre.derecha = y
            
        y.izquierda = z
        z.padre = y
    
    def _rotar_derecha(self, z):
        y = z.izquierda
        z.izquierda = y.derecha
        
        if y.derecha is not None:
            y.derecha.padre = z
        
        y.padre = z.padre
        
        if z.padre is None:
            self.raiz = y
        elif z == z.padre.derecha:
            z.padre.derecha = y
        else:
            z.padre.izquierda = y
            
        y.derecha = z
        z.padre = y
    
    # Busqueda:
    def buscar(self, clave):
        return self._buscar_rec(self.raiz, clave)
    
    def _buscar_rec(self, nodo, clave):
        if nodo is None:
            return False
        if clave == nodo.clave:
            return True
        if clave < nodo.clave:
            return self._buscar_rec(nodo.izquierda, clave)
        return self._buscar_rec(nodo.derecha, clave)
    
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
    
    # Imprimir.
    def _imprimir_arbol(self, nodo=None, prefijo="", es_derecha=True, primer_llamado=True):
        if primer_llamado:
            nodo = self.raiz
            if nodo is None:
                print("(Árbol vacío)")
                return
            color = "R" if nodo.color == ROJO else "N"
            print(f"[{nodo.clave}|{color}]")
            self._imprimir_arbol(nodo.derecha, "", True, False)
            self._imprimir_arbol(nodo.izquierda, "", False, False)
            return
        
        if nodo is None:
            return
        
        conector = "└── " if es_derecha else "├── "
        lado = "D" if es_derecha else "I"
        color = "R" if nodo.color == ROJO else "N"
        print(f"{prefijo}{conector}[{nodo.clave}|{color}] {lado}")
        
        extension = "    " if es_derecha else "│   "
        self._imprimir_arbol(nodo.derecha,  prefijo + extension, True, False)
        self._imprimir_arbol(nodo.izquierda,    prefijo + extension, False, False)
                