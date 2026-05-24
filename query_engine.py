from storage_manager import StorageManager

class QueryEngine:
    def __init__(self):
        self.sm = StorageManager()
        self.arbol_activo = "auto"

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
            elif op == "SHOW" and len(partes) > 1 and partes[1].upper() == "TREE":
                return self._show_tree(partes[2:])
            elif op == "USE" and len(partes) > 1 and partes[1].upper() == "TREE":
                return self._use_tree(partes[2:])
            elif op == "INFO":
                return {"tipo": "info", "datos": [self.sm.info()]}
            elif op == "HELP":
                return self._help(partes[1:])
            else:
                return {"error": f"Comando desconocido: '{op}'"}
        except Exception as e:
            return {"error": str(e)}
        
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
                valor = int(valor)
            except ValueError:
                try:
                    valor = float(valor)
                except ValueError:
                    pass
            datos[campo] = valor
        registro = self.sm.insert(datos)
        return {"tipo": "insert", "datos": [registro]}

    def _select(self, partes):
        if len(partes) < 3 or partes[1] != "=":
            return {"error": "Formato: SELECT campo = valor"}
        campo = partes[0]
        valor = partes [2]
        try:
            valor = int(valor)
        except ValueError:
            try:
                valor = float(valor)
            except ValueError:
                pass
        resultado = self.sm.select(campo, valor)
        return {"tipo": "select", "datos": resultado}

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
        return {"tipo": "range", "datos": resultado}
    
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
        return {"tipo": "delete", "datos": [], "mensaje": f"{n} registro(s) eliminado(s)"}
    
    def _index(self, partes):
        if not partes:
            return {"error": "INDEX require un campo. Ej: INDEX ciudad"}
        mensaje = self.sm.index(partes[0])
        return {"tipo": "index", "datos": [], "mensaje": mensaje}
    
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
    
    def _help(self, partes):
        temas = {
            "": """
🌿 TRESDB — Comandos disponibles:
        INSERT campo:valor campo:valor ...
        SELECT campo = valor
        RANGE  campo inicio fin
        DELETE campo = valor
        INDEX  campo
        SHOW TREE [avl|rn|b|bmas]
        USE TREE  [avl|rn|b|bmas|auto]
        INFO
        HELP [INSERT|SELECT|RANGE|DELETE|INDEX|TREES]
""",
            "INSERT": "🌱 INSERT nombre:Ana edad:25\n  Guarda un registro con los campos que definas.",
            "SELECT": "🔍 SELECT nombre = Ana\n  Busca registros donde el campo tenga ese valor exacto.",
            "RANGE":  "↔ RANGE edad 20 30\n  Busca registros donde el campo esté entre dos valores.",
            "DELETE": "🍂 DELETE nombre = Ana\n  Elimina todos los registros que coincidan.",
            "INDEX":  "📌 INDEX ciudad\n  Crea un índice secundario para búsquedas más rápidas.",
            "TREES":  """🌳 Los 4 árboles de TRESDB:
  AVL    → índice primario, búsqueda exacta O(log n)
  R-N    → índices secundarios, inserciones masivas
  B      → organización de bloques internos
  B+     → almacén principal, soporta RANGE por hojas enlazadas""",
        }
        clave = partes[0].upper() if partes else ""
        texto = temas.get(clave, f"No hay ayuda para '{clave}'. Escribe HELP para ver todo.")
        return {"tipo": "help", "datos": [], "mensaje": texto}