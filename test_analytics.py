import sqlite3
import pandas as pd
import pytest
from analytics import load_data, metrics, monthly
from build_database import build

def test_metrics_exclude_cancellations_and_count_orders_once():
    data = pd.DataFrame({"pedido_id":[1,1,2], "status":["Concluído","Concluído","Cancelado"], "receita_centavos":[10000,5000,99999], "lucro_centavos":[3000,1000,99999]})
    result = metrics(data)
    assert result["receita"] == 150
    assert result["pedidos"] == 1
    assert result["ticket"] == 150
    assert result["margem"] == pytest.approx(40/150)
    empty = metrics(data.iloc[:0])
    assert empty["ticket"] is None and empty["margem"] is None

def test_sql_and_python_reconcile(tmp_path):
    data = load_data()
    path = build(tmp_path / "vendas.db")
    with sqlite3.connect(path) as db:
        total, orders = db.execute("SELECT SUM(receita_centavos)/100.0,COUNT(DISTINCT pedido_id) FROM fato_venda WHERE status='Concluído'").fetchone()
        assert not db.execute("PRAGMA foreign_key_check").fetchall()
    assert metrics(data)["receita"] == total
    assert metrics(data)["pedidos"] == orders
    assert monthly(data).receita.sum() == pytest.approx(total)
    assert (data.lucro_centavos == data.receita_centavos - data.custo_centavos).all()

def test_ui_filters_handle_empty_selection():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file("app.py").run(timeout=20)
    assert not app.exception
    app.sidebar.multiselect[0].set_value([]).run()
    assert not app.exception
    assert app.info
