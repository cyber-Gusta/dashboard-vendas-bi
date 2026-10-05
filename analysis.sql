-- SQLite. Valores financeiros armazenados em centavos inteiros.
SELECT substr(data,1,7) AS mes,
       SUM(receita_centavos)/100.0 AS receita_liquida,
       SUM(lucro_centavos)/100.0 AS lucro_bruto,
       1.0*SUM(lucro_centavos)/NULLIF(SUM(receita_centavos),0) AS margem_bruta,
       COUNT(DISTINCT pedido_id) AS pedidos,
       SUM(receita_centavos)/100.0/NULLIF(COUNT(DISTINCT pedido_id),0) AS ticket_medio
FROM fato_venda WHERE status='Concluído' GROUP BY 1 ORDER BY 1;

SELECT categoria, SUM(receita_centavos)/100.0 AS receita_liquida
FROM vw_vendas WHERE status='Concluído' GROUP BY categoria ORDER BY receita_liquida DESC;
