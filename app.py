from flask import Flask, render_template, request, jsonify
from query_engine import QueryEngine
import io, sys

app = Flask(__name__)
qe  = QueryEngine()

def capturar_arbol(arbol):
    """Captura la salida de _imprimir_arbol como lista de líneas"""
    buffer = io.StringIO()
    sys.stdout = buffer
    arbol._imprimir_arbol()
    sys.stdout = sys.__stdout__
    salida = buffer.getvalue()
    return [l for l in salida.split('\n') if l.strip()]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    comando = request.json.get("comando", "")
    resultado = qe.ejecutar(comando)
    return jsonify(resultado)

@app.route("/info")
def info():
    return jsonify(qe.sm.info())

@app.route("/tree/<tab>")
def get_tree(tab):
    sm = qe.sm
    try:
        if tab == 'avl':
            lineas = capturar_arbol(sm.avl)
        elif tab == 'rn':
            lineas = capturar_arbol(sm.rn)
        elif tab == 'b':
            lineas = capturar_arbol(sm.b)
        elif tab == 'bmas':
            lineas = capturar_arbol(sm.bmas)
        else:
            lineas = []
    except:
        lineas = []
    return jsonify({"lineas": lineas})

if __name__ == "__main__":
    app.run(debug=True)