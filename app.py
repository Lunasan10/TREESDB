import io
from contextlib import redirect_stdout
from flask import Flask, render_template, request, jsonify
from query_engine import QueryEngine

app = Flask(__name__)
qe  = QueryEngine()

def capturar_arbol(arbol):
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            arbol._imprimir_arbol()
    except Exception as e:
        print(f"[TRESDB] Error capturando árbol: {e}")
        return []
    salida = buffer.getvalue()
    lineas = [l for l in salida.split('\n') if l.strip()]
    if len(lineas) == 1 and 'vacío' in lineas[0].lower():
        return []
    return lineas

def altura(nodo):
    return nodo.altura if nodo else 0

def arbol_a_json(nodo, tipo='avl'):
    if nodo is None:
        return None
    if tipo == 'avl':
        fb = altura(nodo.derecha) - altura(nodo.izquierda)
        return {
            "clave":     nodo.clave,
            "fb":        fb,
            "altura":    nodo.altura,
            "izquierda": arbol_a_json(nodo.izquierda, tipo),
            "derecha":   arbol_a_json(nodo.derecha, tipo)
        }
    if tipo == 'rn':
        return {
            "clave":     nodo.clave,
            "color":     "R" if nodo.color == 0 else "N",
            "izquierda": arbol_a_json(nodo.izquierda, tipo),
            "derecha":   arbol_a_json(nodo.derecha, tipo)
        }
    return None

def arbol_b_a_json(nodo):
    if nodo is None:
        return None
    return {
        "claves": nodo.claves,
        "hoja":   nodo.hoja,
        "hijos":  [arbol_b_a_json(h) for h in nodo.hijos]
    }

@app.route("/tree-json/<tab>")
def get_tree_json(tab):
    sm = qe.sm
    try:
        if tab == 'avl':
            raiz = sm.avl.raiz
            data = arbol_a_json(raiz, 'avl') if raiz and raiz.clave is not None else None
        elif tab == 'rn':
            raiz = sm.rn.raiz
            data = arbol_a_json(raiz, 'rn') if raiz else None
        elif tab == 'b':
            raiz = sm.b.raiz
            data = arbol_b_a_json(raiz) if raiz and raiz.claves else None
        elif tab == 'bmas':
            raiz = sm.bmas.raiz
            data = arbol_b_a_json(raiz) if raiz and raiz.claves else None
        else:
            data = None
    except Exception as e:
        print(f"[TRESDB] Error serializando árbol '{tab}': {e}")
        data = None
    return jsonify({"arbol": data})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        data = {}
    comando = data.get("comando", "")
    resultado = qe.ejecutar(comando)
    return jsonify(resultado)

@app.route("/info")
def info():
    datos = qe.sm.info()
    datos["tabla"] = qe.tabla_activa   # ← agregar esta línea
    return jsonify(datos)

@app.route("/tree/<tab>")
def get_tree(tab):
    sm = qe.sm
    arboles = {
        'avl':  sm.avl,
        'rn':   sm.rn,
        'b':    sm.b,
        'bmas': sm.bmas,
    }
    arbol = arboles.get(tab)
    if arbol is None:
        return jsonify({"lineas": []})
    try:
        lineas = capturar_arbol(arbol)
    except Exception as e:
        app.logger.exception("Error al obtener árbol '%s': %s", tab, e)
        lineas = []
    return jsonify({"lineas": lineas})

if __name__ == "__main__":
    app.run(debug=True)