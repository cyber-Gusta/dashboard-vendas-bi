PRAGMA foreign_keys = ON;
CREATE TABLE dim_cliente (cliente_id INTEGER PRIMARY KEY, cliente TEXT NOT NULL, regiao TEXT NOT NULL, segmento TEXT NOT NULL);
CREATE TABLE dim_produto (produto_id INTEGER PRIMARY KEY, produto TEXT NOT NULL, categoria TEXT NOT NULL);
CREATE TABLE fato_venda (
    item_id INTEGER PRIMARY KEY, pedido_id INTEGER NOT NULL, data TEXT NOT NULL,
    cliente_id INTEGER NOT NULL REFERENCES dim_cliente(cliente_id),
    produto_id INTEGER NOT NULL REFERENCES dim_produto(produto_id),
    canal TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('Concluído','Cancelado')),
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    receita_centavos INTEGER NOT NULL, custo_centavos INTEGER NOT NULL, lucro_centavos INTEGER NOT NULL,
    CHECK(lucro_centavos = receita_centavos - custo_centavos)
);
CREATE INDEX idx_venda_data ON fato_venda(data);
CREATE VIEW vw_vendas AS SELECT f.*, c.cliente, c.regiao, c.segmento, p.produto, p.categoria
FROM fato_venda f JOIN dim_cliente c USING(cliente_id) JOIN dim_produto p USING(produto_id);
