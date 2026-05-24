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
    
    # árbol vacío → devolver [] para que el frontend muestre el placeholder
    if len(lineas) == 1 and 'vacío' in lineas[0].lower():
        return []
    
    return lineas

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
    return jsonify(qe.sm.info())

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
        app.logger.exception("Error al obtener el árbol para tab '%s': %s", tab, e)
        lineas = []
    
    return jsonify({"lineas": lineas})

if __name__ == "__main__":
    app.run(debug=True)