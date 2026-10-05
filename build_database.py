"""Carrega o CSV em SQLite. Recria apenas vendas.db ao executar."""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build(path=ROOT / "vendas.db"):
    rows = list(csv.DictReader((ROOT / "vendas.csv").open(encoding="utf-8")))
    path = Path(path)
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as db:
        db.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
        customers = {r["cliente_id"]:(r["cliente_id"],r["cliente"],r["regiao"],r["segmento"]) for r in rows}
        products = {r["produto_id"]:(r["produto_id"],r["produto"],r["categoria"]) for r in rows}
        db.executemany("INSERT INTO dim_cliente VALUES (?,?,?,?)", customers.values())
        db.executemany("INSERT INTO dim_produto VALUES (?,?,?)", products.values())
        columns = ["item_id","pedido_id","data","cliente_id","produto_id","canal","status","quantidade","receita_centavos","custo_centavos","lucro_centavos"]
        db.executemany("INSERT INTO fato_venda VALUES (?,?,?,?,?,?,?,?,?,?,?)", [[r[c] for c in columns] for r in rows])
        print("SQLite carregado:", len(rows), "itens de venda")
    return path

if __name__ == "__main__":
    build()
