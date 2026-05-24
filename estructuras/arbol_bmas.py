class NodoBMas:
    def __init__(self, hoja=True):
        self.claves = []
        self.hijos = []
        self.hoja = hoja
        self.siguiente = None
    
class ArbolBMas:
    def __init__(self, t=2):
        self.raiz = NodoBMas(hoja=True)
        self.t = t
        self.primera_hoja = self.raiz
    
    # Búsqueda
    def buscar(self, clave):
        return self._buscar_rec(self.raiz, clave)
    
    def _buscar_rec(self, nodo, clave):
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if nodo.hoja:
            if i < len(nodo.claves) and nodo.claves[i] == clave:
                return True
            return False

        # en nodos internos solo navegamos
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            i += 1
        return self._buscar_rec(nodo.hijos[i], clave)
    
    # Insertar:
    def _split_hoja(self, padre, i):
        t    = self.t
        hijo = padre.hijos[i]

        nuevo        = NodoBMas(hoja=True)
        nuevo.claves = hijo.claves[t:]
        hijo.claves  = hijo.claves[:t]      

        nuevo.siguiente = hijo.siguiente
        hijo.siguiente  = nuevo

        # la primera clave del nuevo sube al padre -> se compia
        padre.claves.insert(i, nuevo.claves[0])
        padre.hijos.insert(i + 1, nuevo)

    def _split_interno(self, padre, i):
        t    = self.t
        hijo = padre.hijos[i]

        nuevo           = NodoBMas(hoja=False)
        clave_media     = hijo.claves[t - 1]

        nuevo.claves    = hijo.claves[t:]
        hijo.claves     = hijo.claves[:t - 1]
        nuevo.hijos     = hijo.hijos[t:]
        hijo.hijos      = hijo.hijos[:t]

        # la clave media sube al padre 
        padre.claves.insert(i, clave_media)
        padre.hijos.insert(i + 1, nuevo)
           
    def insertar(self, clave):
        raiz = self.raiz

        if len(raiz.claves) == 2 * self.t - 1:
            nueva_raiz = NodoBMas(hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            if self.raiz.hoja:
                self._split_hoja(nueva_raiz, 0)
            else:
                self._split_interno(nueva_raiz, 0)
            self.raiz = nueva_raiz

        self._insertar_rec(self.raiz, clave)
        self._actualizar_primera_hoja()

    def _insertar_rec(self, nodo, clave):
        i = len(nodo.claves) - 1

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

            hijo = nodo.hijos[i]
            if len(hijo.claves) == 2 * self.t - 1:
                if hijo.hoja:
                    self._split_hoja(nodo, i)
                else:
                    self._split_interno(nodo, i)
                if clave >= nodo.claves[i]:
                    i += 1

            self._insertar_rec(nodo.hijos[i], clave)

    def _actualizar_primera_hoja(self):
        nodo = self.raiz
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        self.primera_hoja = nodo 
        
    # Rango:
    def rango(self, inicio, fin):
        # encontrar la hoja de entrada
        hoja = self._buscar_hoja(self.raiz, inicio)

        resultado = []

        # caminar por la cadena de hojas
        while hoja is not None:
            for clave in hoja.claves:
                if clave > fin:
                    return resultado
                if clave >= inicio:
                    resultado.append(clave)
            hoja = hoja.siguiente

        return resultado

    def _buscar_hoja(self, nodo, clave):
        if nodo.hoja:
            return nodo
        i = 0
        while i < len(nodo.claves) and clave >= nodo.claves[i]:
            i += 1
        return self._buscar_hoja(nodo.hijos[i], clave)

    # Recorrido:
    def en_orden(self):
        resultado = []
        hoja = self.primera_hoja
        while hoja is not None:
            resultado.extend(hoja.claves)
            hoja = hoja.siguiente
        return resultado

    def _imprimir_arbol(self, nodo=None, nivel=0, primer_llamado=True):
        if primer_llamado:
            nodo = self.raiz
        espacio = "  " * nivel
        tipo = "[H]" if nodo.hoja else "[I]"
        print(f"{espacio}{tipo} {nodo.claves}")
        for hijo in nodo.hijos:
            self._imprimir_arbol(hijo, nivel + 1, False)

    def _imprimir_hojas(self):
        hoja = self.primera_hoja
        cadena = []
        while hoja is not None:
            cadena.append(str(hoja.claves))
            hoja = hoja.siguiente
        print(" → ".join(cadena))
        
    # Eliminación:
    def eliminar(self, clave):
        self._eliminar_rec(self.raiz, clave)
        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]
        self._actualizar_primera_hoja()

    def _eliminar_rec(self, nodo, clave):
        t = self.t
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if nodo.hoja:
            # eliminar directo de la hoja
            if i < len(nodo.claves) and nodo.claves[i] == clave:
                nodo.claves.pop(i)
            return

        # nodo interno — solo navegamos
        if i < len(nodo.claves) and nodo.claves[i] == clave:
            i += 1      # ir al hijo derecho

        ultimo = (i == len(nodo.hijos) - 1)

        if len(nodo.hijos[i].claves) < t:
            self._rellenar(nodo, i)
            if ultimo and i > 0:
                i -= 1

        self._eliminar_rec(nodo.hijos[i], clave)

        # actualizar clave de navegación si es necesario
        if i > 0 and len(nodo.hijos[i].claves) > 0:
            nodo.claves[i - 1] = nodo.hijos[i].claves[0]

    def _rellenar(self, padre, i):
        t = self.t
        if i > 0 and len(padre.hijos[i - 1].claves) >= t:
            self._robar_izquierda(padre, i)
        elif i < len(padre.hijos) - 1 and len(padre.hijos[i + 1].claves) >= t:
            self._robar_derecha(padre, i)
        else:
            if i < len(padre.hijos) - 1:
                self._merge(padre, i)
            else:
                self._merge(padre, i - 1)

    def _robar_izquierda(self, padre, i):
        hijo    = padre.hijos[i]
        hermano = padre.hijos[i - 1]

        if hijo.hoja:
            hijo.claves.insert(0, hermano.claves.pop())
            padre.claves[i - 1] = hijo.claves[0]
        else:
            hijo.claves.insert(0, padre.claves[i - 1])
            padre.claves[i - 1] = hermano.claves.pop()
            if not hermano.hoja:
                hijo.hijos.insert(0, hermano.hijos.pop())

    def _robar_derecha(self, padre, i):
        hijo    = padre.hijos[i]
        hermano = padre.hijos[i + 1]

        if hijo.hoja:
            hijo.claves.append(hermano.claves.pop(0))
            padre.claves[i] = hermano.claves[0]
        else:
            hijo.claves.append(padre.claves[i])
            padre.claves[i] = hermano.claves.pop(0)
            if not hermano.hoja:
                hijo.hijos.append(hermano.hijos.pop(0))

    def _merge(self, padre, i):
        hijo_izq = padre.hijos[i]
        hijo_der = padre.hijos[i + 1]

        if hijo_izq.hoja:
            hijo_izq.claves.extend(hijo_der.claves)
            hijo_izq.siguiente = hijo_der.siguiente
        else:
            hijo_izq.claves.append(padre.claves[i])
            hijo_izq.claves.extend(hijo_der.claves)
            hijo_izq.hijos.extend(hijo_der.hijos)

        padre.claves.pop(i)
        padre.hijos.pop(i + 1)