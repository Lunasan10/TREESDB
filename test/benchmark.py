import sys, os, time, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from query_engine import QueryEngine

def medir(fn, repeticiones=1):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        fn()
    fin = time.perf_counter()
    total = (fin - inicio) * 1000
    return total / repeticiones

print("=" * 50)
print("TRESDB — Benchmark")
print("=" * 50)

# ── Setup ─────────────────────────────────────────────
qe = QueryEngine()
random.seed(42)
N = 500

print(f"\nInsertando {N} registros...")
inicio = time.perf_counter()
for i in range(N):
    qe.ejecutar(f"INSERT nombre:user{i} edad:{random.randint(18,80)} ciudad:ciudad{i%10}")
fin = time.perf_counter()
t_insert = (fin - inicio) * 1000
print(f"  INSERT {N} registros → {t_insert:.1f}ms total | {t_insert/N:.3f}ms por registro")

# ── SELECT por id ─────────────────────────────────────
ids = random.sample(range(1, N+1), 50)
t = medir(lambda: [qe.ejecutar(f"SELECT id = {i}") for i in ids])
print(f"\n  SELECT por id (AVL) → {t/50:.3f}ms promedio")

# ── SELECT sin índice ─────────────────────────────────
t = medir(lambda: qe.ejecutar("SELECT ciudad = ciudad3"))
print(f"  SELECT sin índice (B+) → {t:.3f}ms promedio")

# ── INDEX ─────────────────────────────────────────────
t = medir(lambda: QueryEngine())
qe.ejecutar("INDEX ciudad")
t = medir(lambda: qe.ejecutar("SELECT ciudad = ciudad3"))
print(f"  SELECT con índice (R-N) → {t:.3f}ms promedio")

# ── RANGE ─────────────────────────────────────────────
rangos = [(20,30),(18,25),(50,70),(30,60)]
t = medir(lambda: [qe.ejecutar(f"RANGE edad {a} {b}") for a,b in rangos])
print(f"  RANGE edad (B+) → {t/4:.3f}ms promedio")

# ── DELETE ────────────────────────────────────────────
ids_del = random.sample(range(1, N+1), 50)
inicio = time.perf_counter()
for i in ids_del:
    qe.ejecutar(f"DELETE id = {i}")
fin = time.perf_counter()
t_delete = (fin - inicio) * 1000
print(f"  DELETE 50 registros → {t_delete:.1f}ms total | {t_delete/50:.3f}ms por registro")

# ── Resumen ───────────────────────────────────────────
print("\n" + "=" * 50)
print("Resumen")
print("=" * 50)
registros_finales = qe.ejecutar("INFO")["datos"][0]["registros"]
print(f"  Registros finales:  {registros_finales}")
print(f"  Throughput INSERT:  {N / (t_insert/1000):.0f} registros/segundo")
print(f"  Throughput DELETE:  {50 / (t_delete/1000):.0f} registros/segundo")
print("\n🌱 Benchmark completado")