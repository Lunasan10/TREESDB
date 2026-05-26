# 🌳 TRESDB
> *Base de datos basada en árboles auto-balanceados*

Motor de base de datos construido desde cero sobre 4 árboles autobalanceados. Cada operación usa la estructura más eficiente para esa tarea.

🔗 **Demo en vivo:** [treedb.onrender.com](https://treedb.onrender.com)

> ⚠️ La primera visita puede tardar ~30 segundos en despertar el servidor (plan gratuito de Render).

---

## ¿Qué es TRESDB?

Una base de datos que organiza tu información de manera inteligente, como un archivero que siempre sabe exactamente dónde está cada cosa. Construido completamente en Python con una interfaz web interactiva que muestra en tiempo real cómo el sistema organiza los datos por dentro.

---

## Los 4 árboles

| Árbol | Rol | Por qué |
|---|---|---|
| 🟢 **AVL** | Índice primario | Búsqueda exacta O(log n) garantizada |
| 🔴 **Rojo-Negro** | Índices secundarios | Menos rotaciones en inserciones masivas |
| 🟤 **B** | Bloques internos | Agrupa datos eficientemente |
| 🔵 **B+** | Almacén principal | Hojas enlazadas permiten búsqueda por rango |

---

## Comandos

```bash
# Gestión de datos
INSERT nombre:Ana edad:25 ciudad:Bogotá
SELECT nombre = Ana
SELECT id = 3
RANGE  edad 20 30
UPDATE nombre = Ana SET edad:26 ciudad:Medellín
DELETE nombre = Ana

# Gestión de tablas
CREATE TABLE estudiantes nombre:texto edad:entero
DROP TABLE estudiantes
USE TABLE estudiantes
SHOW TABLES

# Índices y utilidades
INDEX ciudad
SHOW TREE avl
USE TREE b+
SAVE estado.json
LOAD estado.json
INFO
HELP
```

---

## Datasets de prueba

Listos para cargar en la interfaz:

```bash
LOAD pequeno.json    # 10 registros — operaciones básicas
LOAD mediano.json    # 100 registros — índices, rangos y rendimiento
```

Comandos sugeridos después de cargar `mediano.json`:

```bash
INDEX departamento
SELECT departamento = Sistemas
RANGE edad 25 35
UPDATE ciudad = Cali SET ciudad:Medellín
DELETE activo = false
```

---

## Benchmark

Medido con 500 registros en Python puro:

| Operación | Rendimiento |
|---|---|
| INSERT | ~32,000 registros/segundo |
| DELETE | ~11,000 registros/segundo |

---

## Stack

- **Backend** — Python 3 + Flask + Gunicorn
- **Estructuras** — AVL, Rojo-Negro, Árbol B, Árbol B+ implementados desde cero
- **Frontend** — HTML + CSS + JS vanilla, visualizador SVG interactivo
- **Persistencia** — JSON con SAVE/LOAD manual
- **Deploy** — Render (plan gratuito)

---

## Instalación local

```bash
git clone https://github.com/Lunasan10/TREESDB.git
cd TREESDB
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000`

---

## Estructura del proyecto
```
TREESDB/
├── app.py                  # servidor Flask
├── query_engine.py         # intérprete de comandos
├── storage_manager.py      # coordinador de los 4 árboles
├── estructuras/
│   ├── avl.py
│   ├── rojo_negro.py
│   ├── arbol_b.py
│   └── arbol_bmas.py
├── static/
│   ├── style.css
│   └── main.js
├── templates/
│   └── index.html
├── data/
│   ├── pequeno.json
│   └── mediano.json
├── datasets/
│   └── generar_mediano.py
├── test/
│   ├── test_avl.py
│   ├── test_rojo_negro.py
│   ├── test_b.py
│   ├── test_bmas.py
│   ├── test_sistema.py
│   └── benchmark.py
├── requirements.txt
└── Procfile
```

---

## Pruebas

```bash
# árboles individuales
python test/test_avl.py
python test/test_rojo_negro.py
python test/test_b.py
python test/test_bmas.py

# sistema completo
python test/test_sistema.py

# benchmark
python test/benchmark.py
```

---

## Desarrollado en fases

| Fase | Módulo |
|---|---|
| 1–2 | AVL completo con rotaciones y delete |
| 3–4 | Rojo-Negro completo |
| 5–6 | Árbol B y B+ con hojas enlazadas |
| 7 | Storage Manager — coordinación de los 4 árboles |
| 8 | Query Engine + GUI web con Flask |
| 9 | Visualizador SVG animado + Help integrado |
| 10 | Tests + Benchmark + Deploy + Documentación |

---

## Equipo

Luna A. Sandoval · Nicolás Rodríguez · Geraldine Vargas

*Proyecto Final — Ciencias de la Computación I · Universidad Distrital*