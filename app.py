import streamlit as st
import plotly.express as px
from analytics import load_data, completed, metrics, monthly, brl, brl_compact

st.set_page_config(page_title="BI de Vendas", page_icon="📊", layout="wide")
st.title("Análise de vendas")
st.caption("Portfólio de Gustavo Mendes. Dados sintéticos de 2025; valores em reais.")
data = load_data()
with st.sidebar:
    st.header("Filtros")
    months = st.multiselect("Mês", sorted(data.mes.unique()), default=sorted(data.mes.unique()))
    regions = st.multiselect("Região", sorted(data.regiao.unique()), default=sorted(data.regiao.unique()))
    categories = st.multiselect("Categoria", sorted(data.categoria.unique()), default=sorted(data.categoria.unique()))
    channels = st.multiselect("Canal", sorted(data.canal.unique()), default=sorted(data.canal.unique()))
filtered = data.loc[data.mes.isin(months) & data.regiao.isin(regions) & data.categoria.isin(categories) & data.canal.isin(channels)]
kpi = metrics(filtered)
a, b, c, d = st.columns(4)
a.metric("Receita líquida", brl_compact(kpi["receita"]), help=brl(kpi["receita"]))
b.metric("Lucro bruto", brl_compact(kpi["lucro"]), help=brl(kpi["lucro"]))
c.metric("Margem bruta", f'{kpi["margem"]:.1%}' if kpi["margem"] is not None else "Sem dados")
d.metric("Pedidos concluídos", kpi["pedidos"])
st.caption(f'Ticket médio no recorte: {brl(kpi["ticket"])}. Pedidos cancelados são excluídos dos indicadores.')
if filtered.empty or completed(filtered).empty:
    st.info("Nenhuma venda concluída para os filtros selecionados.")
    st.stop()
trend = monthly(filtered)
st.plotly_chart(px.line(trend, x="mes", y=["receita", "lucro"], markers=True, title="Receita e lucro bruto por mês", labels={"mes":"Mês", "value":"R$", "variable":"Indicador"}, color_discrete_sequence=["#2563EB", "#7C3AED"]), width="stretch")
left, right = st.columns(2)
valid = completed(filtered)
by_category = valid.groupby("categoria", as_index=False).receita_centavos.sum()
by_category["receita"] = by_category.receita_centavos / 100
by_region = valid.groupby("regiao", as_index=False).receita_centavos.sum()
by_region["receita"] = by_region.receita_centavos / 100
with left:
    st.plotly_chart(px.bar(by_category.sort_values("receita", ascending=False), x="categoria", y="receita", title="Receita por categoria", labels={"categoria":"Categoria", "receita":"R$"}, color_discrete_sequence=["#2563EB"]), width="stretch")
with right:
    st.plotly_chart(px.bar(by_region.sort_values("receita"), x="receita", y="regiao", orientation="h", title="Receita por região", labels={"regiao":"Região", "receita":"R$"}, color_discrete_sequence=["#7C3AED"]), width="stretch")
with st.expander("Consultar os registros filtrados"):
    st.dataframe(filtered, hide_index=True, width="stretch")
    st.download_button("Baixar CSV do recorte", filtered.to_csv(index=False).encode("utf-8-sig"), "vendas_filtradas.csv", "text/csv")
st.caption("O lucro bruto considera apenas receita menos custo de mercadoria. O ticket usa os itens e pedidos presentes no recorte; um filtro de categoria pode representar parte de um pedido.")
