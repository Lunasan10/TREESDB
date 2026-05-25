import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from query_engine import QueryEngine

def test_create_table():
    qe = QueryEngine()
    r = qe.ejecutar("CREATE TABLE usuarios nombre:text edad:int")
    print(r)
    assert r["tipo"] == "create_table", f"Esperado 'create_table', got: {r}"
    assert "usuarios" in qe.tablas
    print("✅ CREATE TABLE OK")

def test_esquema_valida_tipos():
    qe = QueryEngine()
    qe.ejecutar("CREATE TABLE productos nombre:text precio:real")
    qe.ejecutar("USE TABLE productos")

    # Insert válido
    r = qe.ejecutar("INSERT nombre:Laptop precio:1200.5")
    assert r["tipo"] == "insert", f"Insert válido falló: {r}"

    # Insert con tipo incorrecto — precio como text
    r = qe.ejecutar("INSERT nombre:Mouse precio:barato")
    assert "error" in r, f"Debió rechazar tipo incorrecto: {r}"
    print("✅ Validación de tipos OK")

def test_use_table_aislamiento():
    qe = QueryEngine()
    qe.ejecutar("CREATE TABLE a")
    qe.ejecutar("CREATE TABLE b")

    qe.ejecutar("USE TABLE a")
    qe.ejecutar("INSERT nombre:Ana")

    qe.ejecutar("USE TABLE b")
    qe.ejecutar("INSERT nombre:Luis")

    # En tabla b solo debe estar Luis
    qe.ejecutar("USE TABLE b")
    r = qe.ejecutar("SELECT nombre = Luis")
    assert len(r["datos"]) == 1
    assert r["datos"][0]["nombre"] == "Luis"

    # En tabla a solo debe estar Ana
    qe.ejecutar("USE TABLE a")
    r = qe.ejecutar("SELECT nombre = Ana")
    assert len(r["datos"]) == 1
    assert r["datos"][0]["nombre"] == "Ana"

    # Ana no debe aparecer en b
    qe.ejecutar("USE TABLE b")
    r = qe.ejecutar("SELECT nombre = Ana")
    assert len(r["datos"]) == 0
    print("✅ Aislamiento entre tablas OK")

def test_drop_table_vacia_datos():
    qe = QueryEngine()
    qe.ejecutar("CREATE TABLE temporal")
    qe.ejecutar("USE TABLE temporal")
    qe.ejecutar("INSERT nombre:Borrame")

    qe.ejecutar("DROP TABLE temporal")

    # La tabla sigue existiendo pero vacía
    assert "temporal" in qe.tablas
    r = qe.ejecutar("SELECT nombre = Borrame")  # sigue en tabla activa (default)
    # El select va a default porque DROP no cambia tabla_activa
    qe.ejecutar("USE TABLE temporal")
    info = qe.ejecutar("INFO")
    assert info["datos"][0]["registros"] == 0
    print("✅ DROP TABLE (vacía datos) OK")

def test_drop_default_prohibido():
    qe = QueryEngine()
    r = qe.ejecutar("DROP TABLE default")
    assert "error" in r
    print("✅ DROP TABLE default protegido OK")

def test_show_tables():
    qe = QueryEngine()
    qe.ejecutar("CREATE TABLE clientes nombre:text")
    qe.ejecutar("USE TABLE clientes")
    qe.ejecutar("INSERT nombre:Pedro")

    r = qe.ejecutar("SHOW TABLES")
    assert r["tipo"] == "show_tables"
    nombres = [f["tabla"] for f in r["datos"]]
    assert "default" in nombres
    assert "clientes" in nombres

    clientes = next(f for f in r["datos"] if f["tabla"] == "clientes")
    assert clientes["registros"] == 1
    print("✅ SHOW TABLES OK")

def test_use_tabla_inexistente():
    qe = QueryEngine()
    r = qe.ejecutar("USE TABLE fantasma")
    assert "error" in r
    print("✅ USE TABLE inexistente da error OK")

if __name__ == "__main__":
    test_create_table()
    test_esquema_valida_tipos()
    test_use_table_aislamiento()
    test_drop_table_vacia_datos()
    test_drop_default_prohibido()
    test_show_tables()
    test_use_tabla_inexistente()
    print("\n🌿 Todos los tests de tablas pasaron")