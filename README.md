# 🌳 TRESDB
> *Motor de base de datos basado en árboles auto-balanceados*
>>>>>>> parent of 68580ac (fix: Indentation errors in query_engine.py)
=======
# 🌳 TRESDB
> *Motor de base de datos basado en árboles auto-balanceados*
>>>>>>> parent of 68580ac (fix: Indentation errors in query_engine.py)

Motor de base de datos construido desde cero sobre 4 árboles autobalanceados. Cada operación usa la estructura más eficiente para esa tarea.

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
| 🔵 **B+** | Almacén principal | Hojas enlazadas permiten búsqued

---

## Comandos

```bash
INSERT nombre:Ana edad:25 ciudad:Bogotá   # guardar un registro
SELECT nombre = Ana                        # búsqueda exacta
SELECT id = 3                              # búsqueda por id (AVL)
RANGE  edad 20 30                          # búsqueda por rango (B+)
DELETE nombre = Ana                        # eliminar registros
UPDATE nombre = Ana SET ciudad:Bogotá      # actualizar registros
INDEX  ciudad                              # crear índice secundario (Rojo-Negro)
SAVE estado.json                           # guardar estado en JSON
LOAD estado.json                           # cargar estado desde JSON
SHOW TREE avl                              # visualizar un árbol
USE TREE b+                                # forzar árbol manualmente
HELP                                       # manual integrado
INFO                                       # estadísticas del sistema
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

- **Backend** — Python + Flask
- **Estructuras** — AVL, Rojo-Negro, Árbol B, Árbol B+ implementados desde cero
- **Frontend** — HTML + CSS + JS vanilla, visualizador SVG
- **Deploy** — Render

---
## Instalación local

```bash
git clone https://github.com/tu-usuario/TREESDB.git
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
└── test/
├── test_avl.py
├── test_rojo_negro.py
├── test_b.py
├── test_bmas.py
├── test_sistema.py
└── benchmark.py
```
---

## Desarrollado en 10 fases

| Fase | Módulo |
|---|---|
| 1-2 | AVL completo |
| 3-4 | Rojo-Negro completo |
| 5-6 | Árbol B y B+ |
| 7 | Storage Manager |
| 8 | Query Engine + GUI |
| 9 | Animaciones SVG + Help |
| 10 | Tests + Benchmark + Deploy |

---

*Proyecto universitario — Estructuras de Datos*
*Desarrollado por: Luna A. Sandoval, Nicolás Rodríguez y Geraldine Vargas*