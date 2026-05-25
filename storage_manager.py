from estructuras.avl import AVL
from estructuras.rojo_negro import RojoNegro
from estructuras.arbol_b import ArbolB
from estructuras.arbol_bmas import ArbolBMas

class StorageManager:
    def __init__(self):
        # Almacén principal
        self.bmas = ArbolBMas(t=2)
        # Índice primario (id)
        self.avl = AVL()
        # Índices secundarios 
        self.rn = RojoNegro()
        # Bloques internos
        self.b = ArbolB(t=2)
        
        self.registros = {}
        self.indices = {}
        self._siguiente_id = 1
    
    # INSERT
    def insert(self, datos: dict):
        id_nuevo = self._siguiente_id
        self._siguiente_id += 1
        
        registro = {**datos, "id": id_nuevo}
        self.registros[id_nuevo] = registro
        
        # B+ guarda el id en el almacén principal
        self.bmas.insertar(id_nuevo)
        
        # AVL guarda el índice primario
        self.avl.insertar(id_nuevo)
        
        # B registra el bloque
        self.b.insertar(id_nuevo)
        
        # Rojo-negro: actualizar índices secundarios existentes
        for campo, indice in self.indices.items():
            valor = datos.get(campo)
            if valor is not None:
                if valor not in indice:
                    indice[valor] = []
                    self.rn.insertar(f"{campo}:{valor!r}")
                indice[valor].append(id_nuevo)
        
        return registro
    
    # SELECT
    def select(self, campo, valor):
        if campo == "id":
            # Búsqueda directa por AVL
            if self.avl.buscar(valor):
                return [self.registros[valor]]
            return []
        
        if campo in self.indices:
            # Búsqueda por índice secundario (ROji-negro)
            ids = self.indices[campo].get(valor, [])
            return [self.registros[i] for i in ids]
        
        # Búsqueda secuencial por hojas del B+
        return [r for r in self.registros.values() if r.get(campo) == valor]
    
    # RANGE
    def range(self, campo, inicio, fin):
        if campo == "id":
            ids = self.bmas.rango(inicio, fin)
            return [self.registros[i] for i in ids if i in self.registros]

        if campo in self.indices:
            resultado = []
            for valor, ids in self.indices[campo].items():
                if isinstance(valor, (int, float)) and inicio <= valor <= fin:
                    resultado.extend([self.registros[i] for i in ids])
            return sorted(resultado, key=lambda r: r.get(campo))
        
        # Búsqueda secuencial
        return sorted(
            [r for r in self.registros.values()
             if isinstance(r.get(campo), (int, float))
             and inicio <= r.get(campo) <= fin],
            key=lambda r: r.get(campo)
        )
    
    # DELETE
    def delete(self, campo, valor):
        registros_a_eliminar = self.select(campo, valor)

        for registro in registros_a_eliminar:
            id_reg = registro["id"]

            try:
                self.bmas.eliminar(id_reg)
            except Exception as e:
                print(f"[TRESDB] Error eliminando de B+: {e}")
            try:
                self.avl.eliminar(id_reg)
            except Exception as e:
                print(f"[TRESDB] Error eliminando de AVL: {e}")
            try:
                self.b.eliminar(id_reg)
            except Exception as e:
                print(f"[TRESDB] Error eliminando de B: {e}")

            for campo_idx, indice in self.indices.items():
                valor_idx = registro.get(campo_idx)
                if valor_idx in indice:
                    indice[valor_idx] = [i for i in indice[valor_idx] if i != id_reg]
                    if not indice[valor_idx]:
                        del indice[valor_idx]

            del self.registros[id_reg]

        # si quedó vacío, reiniciar los árboles para evitar estado inválido
        if len(self.registros) == 0:
            self.reset()

        return len(registros_a_eliminar)
    
    # INDEX
    def index(self, campo):
        if campo in self.indices:
            return f"Índice '{campo}' ya existente"
        
        indice = {}
        for id_reg, registro in self.registros.items():
            valor = registro.get(campo)
            if valor is not None:
                if valor not in indice:
                    indice[valor] = []
                    self.rn.insertar(f"{campo}:{valor!r}")
                indice[valor].append(id_reg)
        
        self.indices[campo] = indice
        return f"Índice '{campo}' creado sobre {len(indice)} valores únicos"
    
    # INFO
    def info(self):
        return {
            "registros"      : len(self.registros),
            "altura_avl"     : self.avl.raiz.altura if self.avl.raiz else 0,
            "indices"        : list(self.indices.keys()),
            "siguiente_id"   : self._siguiente_id
        }
        
    def reset(self):
        self.bmas          = ArbolBMas(t=2)
        self.avl           = AVL()
        self.rn            = RojoNegro()
        self.b             = ArbolB(t=2)
        self.registros     = {}
        self.indices       = {}
        self._siguiente_id = 1