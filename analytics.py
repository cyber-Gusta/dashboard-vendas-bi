from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent / "vendas.csv"

def load_data(path=DATA):
    data = pd.read_csv(path, parse_dates=["data"])
    required = {"item_id", "pedido_id", "data", "receita_centavos", "custo_centavos", "lucro_centavos", "status"}
    if not required.issubset(data.columns):
        raise ValueError("A base de vendas não contém todas as colunas obrigatórias.")
    if data.item_id.duplicated().any():
        raise ValueError("A base contém item_id duplicado.")
    return data

def completed(data):
    return data.loc[data["status"].eq("Concluído")].copy()

def metrics(data):
    valid = completed(data)
    revenue = int(valid["receita_centavos"].sum()) / 100
    profit = int(valid["lucro_centavos"].sum()) / 100
    orders = int(valid["pedido_id"].nunique())
    return {"receita": revenue, "lucro": profit, "pedidos": orders,
            "margem": profit / revenue if revenue else None,
            "ticket": revenue / orders if orders else None}

def monthly(data):
    valid = completed(data)
    result = valid.groupby("mes", as_index=False).agg(receita_centavos=("receita_centavos", "sum"), lucro_centavos=("lucro_centavos", "sum"), pedidos=("pedido_id", "nunique"))
    result["receita"] = result["receita_centavos"] / 100
    result["lucro"] = result["lucro_centavos"] / 100
    return result.sort_values("mes")

def brl(value):
    if value is None:
        return "Sem dados"
    return "R$ " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def brl_compact(value):
    if abs(value) >= 1_000_000:
        return "R$ " + f"{value/1_000_000:.2f}".replace(".", ",") + " mi"
    if abs(value) >= 1_000:
        return "R$ " + f"{value/1_000:.1f}".replace(".", ",") + " mil"
    return brl(value)
