class NodoB:
    def __init__(self, hoja=True):
        self.claves = []
        self.hijos = []
        self.hoja = hoja

class ArbolB:
    def __init__(self, t=2):
        self.raiz = NodoB(hoja=True)
        self.t = t
    
    # Búsqueda:
    def buscar(self, clave):
        return self._buscar_rec(self.raiz, clave)
    
    def _buscar_rec(self, nodo, clave):
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1
        
        # Se encontro el nodo
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return True
        
        # No esta el nodo que se busca
        if nodo.hoja:
            return False
        
        return self._buscar_rec(nodo.hijos[i], clave)
    
    # Inserción:
    def insertar(self, clave):
        raiz = self.raiz
        
        # Se hace split en caso de que la raíz este llena
        if len(raiz.claves) == 2 * self.t -1:
            nueva_raiz = NodoB(hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._split(nueva_raiz, 0)
            self.raiz = nueva_raiz
            
        self._insertar_no_lleno(self.raiz, clave)
        
    def _insertar_no_lleno(self, nodo, clave):        
        i = len(nodo.claves) -1
        
        if nodo.hoja:
            nodo.claves.append(None)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave
            
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            
            if len(nodo.hijos[i].claves) == 2 * self.t - 1:
                self._split(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            
            self._insertar_no_lleno(nodo.hijos[i], clave)
            
    def _split(self, padre, i):
        t = self.t
        hijo = padre.hijos[i]
        
        nuevo = NodoB(hoja=hijo.hoja)
        clave_media = hijo.claves[t - 1]
        
        nuevo.claves = hijo.claves[t:]
        hijo.claves = hijo.claves[:t - 1]
        
        if not hijo.hoja:
            nuevo.hijos = hijo.hijos[t:]
            hijo.hijos = hijo.hijos[:t]
            
        padre.claves.insert(i, clave_media)
        padre.hijos.insert(i + 1, nuevo)
        
        
    # Eliminar:
    def eliminar(self, clave):
        self._eliminar_rec(self.raiz, clave)
        # Caso especial: Si la raíz se queda sin claves, hacer que el primer hijo sea la nueva raíz
        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]
        
    def _eliminar_rec(self, nodo, clave):
        t = self.t
        i = 0

        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and nodo.claves[i] == clave:
            if nodo.hoja:
                # caso 1: hoja → eliminar directo
                nodo.claves.pop(i)
            else:
                hijo_izq = nodo.hijos[i]
                hijo_der = nodo.hijos[i + 1]

                if len(hijo_izq.claves) >= t:
                    # caso 2a: predecesor — bajar por izquierda
                    predecesor = self._maximo(hijo_izq)
                    nodo.claves[i] = predecesor
                    self._eliminar_rec(hijo_izq, predecesor)

                elif len(hijo_der.claves) >= t:
                    # caso 2b: sucesor — bajar por derecha
                    sucesor = self._minimo(hijo_der)
                    nodo.claves[i] = sucesor
                    self._eliminar_rec(hijo_der, sucesor)

                else:
                    # caso 2c: ambos tienen mínimo → merge y bajar
                    self.merge(nodo, i)
                    self._eliminar_rec(nodo.hijos[i], clave)

        else:
            if nodo.hoja:
                return

            ultimo = (i == len(nodo.hijos) - 1)

            if len(nodo.hijos[i].claves) < t:
                self._rellenar(nodo, i)
                if ultimo and i > 0:
                    i -= 1

            self._eliminar_rec(nodo.hijos[i], clave)

    def _minimo(self, nodo):
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        return nodo.claves[0]

    def _maximo(self, nodo):
        while not nodo.hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]

    def _merge(self, padre, i):
        hijo_izquierdo = padre.hijos[i]
        hijo_derecho = padre.hijos[i + 1]
        clave_media = padre.claves.pop(i)
        padre.hijos.pop(i + 1)
        
        hijo_izquierdo.claves.append(clave_media)
        hijo_izquierdo.claves.extend(hijo_derecho.claves)
        hijo_izquierdo.hijos.extend(hijo_derecho.hijos)
        
    def _rellenar(self, padre, i):
        t = self.t
        if i > 0 and len(padre.hijos[i - 1].claves) >= t:
            self._robar_izquierda(padre, i)
        elif i < len(padre.hijos) - 1 and len(padre.hijos[i + 1].claves) >= t:
            self._robar_derecha(padre, i)
        else:
            if i < len(padre.hijos) - 1:
                if len(padre.hijos[i].claves) != t - 1:
                     raise ValueError(
                         f"hijo izq tiene {len(padre.hijos[i].claves)} claves antes de merge"
                     )
                if len(padre.hijos[i + 1].claves) != t - 1:
                    raise ValueError(
                        f"hijo der tiene {len(padre.hijos[i + 1].claves)} claves antes de merge"
                    )
            else:
                if len(padre.hijos[i - 1].claves) != t - 1:
                     raise ValueError(
                         f"hijo izq tiene {len(padre.hijos[i - 1].claves)} claves antes de merge"
                     )
                if len(padre.hijos[i].claves) != t - 1:
                    raise ValueError(
                        f"hijo der tiene {len(padre.hijos[i].claves)} claves antes de merge"
                    )
                self.merge(padre, i - 1)
    
    def _robar_izquierda(self, padre, i):
        hijo = padre.hijos[i]
        hermano = padre.hijos[i - 1]

        # solo robar si el hijo destino no está lleno
        if len(hijo.claves) >= 2 * self.t - 1:
            return False

        hijo.claves.insert(0, padre.claves[i - 1])
        padre.claves[i - 1] = hermano.claves.pop()

        if not hermano.hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())
        return True

    def _robar_derecha(self, padre, i):
        hijo = padre.hijos[i]
        hermano = padre.hijos[i + 1]

        # solo robar si el hijo destino no está lleno
        if len(hijo.claves) >= 2 * self.t - 1:
            return False

        hijo.claves.append(padre.claves[i])
        padre.claves[i] = hermano.claves.pop(0)

        if not hermano.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))
        return True
    
    
    # Recorrer:
    def en_orden(self):
        resultado = []
        self._en_orden_rec(self.raiz, resultado)
        return resultado
    
    def _en_orden_rec(self, nodo, resultado):
        if nodo.hoja:
            resultado.extend(nodo.claves)
            return
        for i, hijo in enumerate(nodo.hijos):
            self._en_orden_rec(hijo, resultado)
            if i < len(nodo.claves):
                resultado.append(nodo.claves[i])        
    
    # Imprimir:
    def _imprimir_arbol(self, nodo=None, nivel=0, primer_llamado=True):
        if primer_llamado:
            nodo = self.raiz
        espacio = " " * nivel
        print(f"{espacio}[{', '.join(str(c) for c in nodo.claves)}]")
        for hijo in nodo.hijos:
            self._imprimir_arbol(hijo, nivel + 1, False)