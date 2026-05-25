from storage_manager import StorageManager

class QueryEngine:
    def __init__(self):
        self.arbol_activo = "auto"
        self.tablas = {"default": StorageManager()}
        self.tabla_activa = "default"

    def ejecutar(self, comando: str) -> dict:
        comando = comando.strip()
        if not comando:
            return {"error": "Comando vacío"}
        
        partes = comando.split()
        op = partes[0].upper()
        
        try:
            if op == "INSERT":
                return self._insert(partes[1:])
            elif op == "SELECT":
                return self._select(partes[1:])
            elif op == "RANGE":
                return  self._range(partes[1:])
            elif op == "DELETE":
                return self._delete(partes[1:])
            elif op == "INDEX":
                return self._index(partes[1:])
            elif op == "INFO":
                return {"tipo": "info", "datos": [self.sm.info()]}
            elif op == "HELP":
                return self._help(partes[1:])
            elif op == "UPDATE":
                return self._update(partes[1:])
            elif op == "SHOW":
                return self._show(partes[1:])
            elif op == "USE":
                return self._use(partes[1:])
            elif op == "CREATE" and len(partes) > 1 and partes[1].upper() == "TABLE":
                return self._create_table(partes[2:])
            elif op == "DROP" and len(partes) > 1 and partes[1].upper() == "TABLE":
                return self._drop_table(partes[2:])
            else:
                return {"error": f"Comando desconocido: '{op}'"}
        except Exception as e:
            return {"error": str(e)}
        
    @property
    def sm(self):
        return self.tablas[self.tabla_activa]

    def _parse_valor(self, campo, valor):
        if self.sm.esquema.get(campo) == "bool":
            valor_normalizado = valor.lower()
            if valor_normalizado in {"true", "1"}:
                return True
            if valor_normalizado in {"false", "0"}:
                return False
        return valor
        
    # parsers
    def _insert(self, partes):
        if not partes:
            return {"error": "INSERT requiere campos. Ej: INSERT nombre:Ana edad:25"}
        datos = {}
        for parte in partes:
            if ":" not in parte:
                return {"error": f"Formato inválido: '{parte}'. Usa campo:valor"}
            campo, valor = parte.split(":", 1)
            try:
                valor = self._parse_valor(campo, valor)
                if isinstance(valor, str):
                    valor = int(valor)
            except ValueError:
                try:
                    valor = float(valor)
                except ValueError:
                    pass
            datos[campo] = valor
        registro = self.sm.insert(datos)
        return {"tipo": "insert", "datos": [registro], "arbol": "AVL + B+"}

    def _select(self, partes):
        if len(partes) < 3 or partes[1] != "=":
            return {"error": "Formato: SELECT campo = valor"}
        campo = partes[0]
        valor = partes[2]
        try:
            valor = int(valor)
        except ValueError:
            try:
                valor = float(valor)
            except ValueError:
                pass
        resultado = self.sm.select(campo, valor)
        arbol = "AVL" if campo == "id" else "Rojo-Negro" if campo in self.sm.indices else "B+"
        return {"tipo": "select", "datos": resultado, "arbol": arbol}

    def _range(self, partes):
        if len(partes) < 3:
            return {"error": "Formato: RANGE campo inicio fin"}
        campo = partes[0]
        try:
            inicio = float(partes[1])
            fin = float(partes[2])
        except ValueError:
            return {"error": "inicio y fin deben ser números"}
        resultado = self.sm.range(campo, inicio, fin)
        return {"tipo": "range", "datos": resultado, "arbol": "B+"}
    
    def _delete(self, partes):
        if len(partes) != 3:
            return {"error": "Formato: DELETE campo = valor"}
        if partes[1] != "=":
            return {"error": "Formato: DELETE campo = valor"}
        campo = partes[0]
        valor = partes[2]
        try:
            valor = int(valor)
        except ValueError:
            try:
                valor = float(valor)
            except ValueError:
                pass
        n = self.sm.delete(campo, valor)
        return {"tipo": "delete", "datos": [], "mensaje": f"{n} registro(s) eliminado(s)", "arbol": "AVL + Rojo-Negro"}
    
    def _index(self, partes):
        if not partes:
            return {"error": "INDEX require un campo. Ej: INDEX ciudad"}
        mensaje = self.sm.index(partes[0])
        return {"tipo": "index", "datos": [], "mensaje": mensaje, "arbol": "Rojo-Negro"}

    def _show(self, partes):
        if not partes:
            return {"error": "Uso: SHOW TREE <árbol> | SHOW TABLES"}
        objetivo = partes[0].upper()
        if objetivo == "TREE":
            return self._show_tree(partes[1:])
        if objetivo == "TABLES":
            return self._show_tables()
        return {"error": "Uso: SHOW TREE <árbol> | SHOW TABLES"}

    def _use(self, partes):
        if not partes:
            return {"error": "Uso: USE TREE <árbol> | USE TABLE <nombre>"}
        objetivo = partes[0].upper()
        if objetivo == "TREE":
            return self._use_tree(partes[1:])
        if objetivo == "TABLE":
            return self._use_table(partes[1:])
        return {"error": "Uso: USE TREE <árbol> | USE TABLE <nombre>"}
    
    def _show_tree(self, partes):
        arboles = {"avl", "rn", "b", "bmas", "b+"}
        if not partes or partes[0].lower() not in arboles:
            return {"error": f"Árboles disponibles: {arboles}"}
        return {"tipo": "show_tree", "arbol": partes[0].lower(), "datos": []}
    
    def _use_tree(self, partes):
        arboles = {"avl", "rn", "b", "bmas", "auto"}
        if not partes or partes[0].lower() not in arboles:
            return {"error": f"Opciones: {sorted(arboles)}"}
        self.arbol_activo = partes[0].lower()
        return {
            "tipo":    "use_tree",
            "arbol":   self.arbol_activo,
            "datos":   [],
            "mensaje": f"Árbol activo: {self.arbol_activo.upper()}"
        }
        
    def _update(self, partes):
        if len(partes) < 5 or partes[1] != "=" or partes[3].upper() != "SET":
            return {"error": "Formato: UPDATE campo = valor SET campo1:valor1 campo2:valor2"}
        
        campo = partes[0]
        valor = partes[2]
        try:
            valor = self._parse_valor(campo, valor)
            if isinstance(valor, str):
                valor = int(valor)
        except ValueError:
            try:
                valor = float(valor)
            except ValueError:
                pass
            
        actualizaciones = {}
        for parte in partes[4:]:
            if ":" not in parte:
                return {"error": f"Formato inválido en SET: '{parte}'. Usa campo:valor"}
            k, v = parte.split(":", 1)
            try:
                v = self._parse_valor(k, v)
                if isinstance(v, str):
                    v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass
            actualizaciones[k] = v
            
        if not actualizaciones:
            return {"error": "SET requiere al menos un campo a actualizar"}
        
        n = self.sm.update(campo, valor, actualizaciones)
        return{
            "tipo":    "update",
            "datos":   [],
            "mensaje": f"{n} registro(s) actualizado(s)",
            "arbol":   "AVL + Rojo-Negro"
        }
    
    # CREATE TABLE:
    def _create_table(self, partes):
        if not partes:
            return {"error": "Uso: CREATE TABLE nombre [campo:tipo ...]"}
        nombre = partes[0].lower()
        if nombre in self.tablas:
            return {"error": f"La tabla '{nombre}' ya existe"}
        
        sm_nuevo = StorageManager()
        
        # esquema opcional
        if len(partes) > 1:
            campos = {}
            for parte in partes[1:]:
                if ":" not in parte:
                    return {"error": f"Formato de esquema inválido: '{parte}'. Usa campo:tipo"}
                campo, tipo = parte.split(":", 1)
                campos[campo] = tipo
            try:
                sm_nuevo.definir_esquema(campos)
            except ValueError as e:
                return {"error": str(e)}
        
        self.tablas[nombre] = sm_nuevo
        esquema = sm_nuevo.esquema or "(sin esquema fijo)"
        return {
            "tipo":    "create_table",
            "datos":   [],
            "mensaje": f"Tabla '{nombre}' creada. Esquema: {esquema}",
            "tabla":   nombre,
            "arbol": "Rojo-Negro",
        }

    # DROP = reset(), NO delete:
    def _drop_table(self, partes):
        if not partes:
            return {"error": "Uso: DROP TABLE nombre"}
        nombre = partes[0].lower()
        if nombre not in self.tablas:
            return {"error": f"La tabla '{nombre}' no existe"}
        if nombre == "default":
            return {"error": "No se puede eliminar la tabla 'default'"}
        self.tablas[nombre].reset()  # vacía datos, árboles se reconstruyen
        esquema_guardado = self.tablas[nombre].esquema  # reset() limpia esquema también
        return {
            "tipo":    "drop_table",
            "datos":   [],
            "mensaje": f"Tabla '{nombre}' vaciada (esquema eliminado)",
            "tabla":   self.tabla_activa,
            "arbol": "-"
        }

    def _use_table(self, partes):
        if not partes:
            return {"error": "Uso: USE TABLE nombre"}
        nombre = partes[0].lower()
        if nombre not in self.tablas:
            return {"error": f"Tabla '{nombre}' no existe. Usa CREATE TABLE primero"}
        self.tabla_activa = nombre
        return {
            "tipo":    "use_table",
            "datos":   [],
            "mensaje": f"Tabla activa: '{nombre}'",
            "tabla":   nombre,
            "arbol": "-"
        }

    def _show_tables(self):
        filas = [
            {
                "tabla":     nombre,
                "registros": sm.info()["registros"],
                "esquema":   sm.info()["esquema"] or "(libre)",
                "activa":    nombre == self.tabla_activa,
            }
            for nombre, sm in self.tablas.items()
        ]
        return {"tipo": "show_tables", "datos": filas, "arbol": "-"}
    
    def _help(self, partes):
        temas = {
            "": """
🌿 TRESDB — Comandos disponibles:
        INSERT campo:valor campo:valor ...
        SELECT campo = valor
        RANGE  campo inicio fin
        DELETE campo = valor
        UPDATE campo = valor SET campo1:valor1 campo2:valor2
        INDEX  campo
        SHOW TREE [avl|rn|b|bmas]
        USE TREE  [avl|rn|b|bmas|auto]
        INFO
        HELP [INSERT|SELECT|RANGE|DELETE|UPDATE|INDEX|TREES]
""",
            "INSERT": "🌱 INSERT nombre:Ana edad:25\n  Guarda un registro con los campos que definas.",
            "SELECT": "🔍 SELECT nombre = Ana\n  Busca registros donde el campo tenga ese valor exacto.",
            "RANGE":  "↔ RANGE edad 20 30\n  Busca registros donde el campo esté entre dos valores.",
            "DELETE": "🍂 DELETE nombre = Ana\n  Elimina todos los registros que coincidan.",
            "INDEX":  "📌 INDEX ciudad\n  Crea un índice secundario para búsquedas más rápidas.",
            "UPDATE": "🛠️ UPDATE nombre = Ana SET edad:26 ciudad:Medellín\n  Actualiza campos en los registros que coincidan.",
            "TREES":  """🌳 Los 4 árboles de TRESDB:
  AVL    → índice primario, búsqueda exacta O(log n)
  R-N    → índices secundarios, inserciones masivas
  B      → organización de bloques internos
  B+     → almacén principal, soporta RANGE por hojas enlazadas""",
        }
        clave = partes[0].upper() if partes else ""
        texto = temas.get(clave, f"No hay ayuda para '{clave}'. Escribe HELP para ver todo.")
        return {"tipo": "help", "datos": [], "mensaje": texto}