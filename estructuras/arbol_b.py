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
        
        # Se hae split en caso de que la raíz este llena
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
            nuevo.hjos = hijo.hijos[t:]
            hijo.hijos = hijo.hijos[:t]
            
        padre.claves.insert(i, clave_media)
        padre.hijos.insert(i + 1, nuevo)
        
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