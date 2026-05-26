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
        
        self.esquema = {}
    
    # INSERT:
    def insert(self, datos: dict):
        self._validar_registro(datos)
        
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
    
    # SELECT:
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
    
    # RANGE:
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
    
    # DELETE:
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
                        self.rn.eliminar(f"{campo_idx}:{valor_idx!r}")

            del self.registros[id_reg]

        # si quedó vacío, reiniciar los árboles para evitar estado inválido
        if len(self.registros) == 0:
            self.reset()

        return len(registros_a_eliminar)
    
    # INDEX:
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
    
    # UPDATE:
    def update(self, campo, valor, actualizaciones: dict):
        registros_a_actualizar = self.select(campo, valor)
        
        if not registros_a_actualizar:
            return 0

        actualizaciones = {k: v for k, v in actualizaciones.items() if k != "id"}

        for registro in registros_a_actualizar:
            registro_actualizado = {**registro, **actualizaciones}
            self._validar_registro(registro_actualizado)
        
        for registro in registros_a_actualizar:
            id_reg = registro["id"]
            
            for campo_upd, valor_upd in actualizaciones.items():
                valor_viejo = registro.get(campo_upd)
                
                if campo_upd in self.indices:
                    indice = self.indices[campo_upd]
                    if valor_viejo in indice:
                        indice[valor_viejo] = [i for i in indice[valor_viejo] if i != id_reg]
                        if not indice[valor_viejo]:
                            del indice[valor_viejo]
                            self.rn.eliminar(f"{campo_upd}:{valor_viejo!r}")
                    if valor_upd not in indice:
                        indice[valor_upd] = []
                        self.rn.insertar(f"{campo_upd}:{valor_upd!r}")
                    indice[valor_upd].append(id_reg)
            
                self.registros[id_reg][campo_upd] = valor_upd
            
        return len(registros_a_actualizar)
    
    # CREATE:
    def definir_esquema(self, campos: dict):
        tipos_validos = {"int", "text", "real", "bool"}
        for campo, tipo in campos.items():
            if tipo not in tipos_validos:
                raise ValueError(f"Tipo inválido '{tipo}'. Usa: {tipos_validos}")
        self.esquema = campos
        
    def _validar_registro(self, datos: dict):
        if not self.esquema:
            return
        for campo, tipo in self.esquema.items():
            if campo not in datos:
                continue
            valor = datos[campo]
            if tipo == "int" and not isinstance(valor, int):
                raise TypeError(f"'{campo}' debe ser entero, recibió {type(valor).__name__}")
            elif tipo == "real" and not isinstance(valor, (int, float)):
                raise TypeError(f"'{campo}' debe ser real, recibió {type(valor).__name__}")
            elif tipo == "text" and not isinstance(valor, str):
                raise TypeError(f"'{campo}' debe ser text, recibió {type(valor).__name__}")
            elif tipo == "bool" and not isinstance(valor, bool):
                raise TypeError(f"'{campo}' debe ser bool, recibió {type(valor).__name__}")
    
    # INFO:
    def info(self):
        return {
            "registros"      : len(self.registros),
            "altura_avl"     : self.avl.raiz.altura if self.avl.raiz else 0,
            "indices"        : list(self.indices.keys()),
            "siguiente_id"   : self._siguiente_id,
            "esquema"        : self.esquema,
        }
        
    def to_dict(self):
        return {
            "esquema": self.esquema,
            "siguiente_id": self._siguiente_id,
            "registros": list(self.registros.values()),
            "indices": list(self.indices.keys()),
        }

    def load_dict(self, data: dict):
        if not isinstance(data, dict):
            raise TypeError("El estado debe ser un diccionario válido")

        self.reset()
        self.esquema = data.get("esquema", {}) or {}

        registros = data.get("registros", [])
        if not isinstance(registros, list):
            raise TypeError("'registros' debe ser una lista")

        for registro in registros:
            if not isinstance(registro, dict) or "id" not in registro:
                raise ValueError("Cada registro debe ser un diccionario con campo 'id'")

            id_reg = registro["id"]
            if not isinstance(id_reg, int) or id_reg <= 0:
                raise ValueError("El campo 'id' debe ser un entero positivo")
            if id_reg in self.registros:
                raise ValueError(f"ID duplicado en la carga: {id_reg}")

            self.registros[id_reg] = registro
            self.bmas.insertar(id_reg)
            self.avl.insertar(id_reg)
            self.b.insertar(id_reg)

        if self.registros:
            self._siguiente_id = max(self.registros.keys()) + 1
        else:
            self._siguiente_id = 1

        siguiente_id = data.get("siguiente_id")
        if isinstance(siguiente_id, int) and siguiente_id > self._siguiente_id:
            self._siguiente_id = siguiente_id

        indices = data.get("indices", [])
        if not isinstance(indices, list):
            raise TypeError("'indices' debe ser una lista")

        for campo in indices:
            if not isinstance(campo, str):
                raise ValueError("Cada índice debe ser un string")
            try:
                self.index(campo)
            except (TypeError, ValueError, KeyError) as exc:
                raise ValueError(f"No se pudo reconstruir el índice '{campo}'") from exc

        return len(self.registros)

    def reset(self):
        self.bmas          = ArbolBMas(t=2)
        self.avl           = AVL()
        self.rn            = RojoNegro()
        self.b             = ArbolB(t=2)
        self.registros     = {}
        self.indices       = {}
        self._siguiente_id = 1