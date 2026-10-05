# Dicionário de dados

Grão: Um item por pedido; pedido_id pode aparecer em várias linhas.

Origem: dados sintéticos, semente 42, período de 2025. Identificadores e valores não representam pessoas ou resultados empresariais reais.

| Campo | Tipo | Definição |
| --- | --- | --- |
| `item_id` | Inteiro | Chave única da linha de venda. |
| `pedido_id` | Inteiro | Identificador do pedido; pode repetir em vários itens. |
| `data` | Data ISO | Data do pedido, em YYYY-MM-DD. |
| `mes` | Texto | Mês da venda ou abertura, em YYYY-MM, ordenável cronologicamente. |
| `cliente_id` | Inteiro | Identificador fictício do cliente. |
| `cliente` | Texto | Nome demonstrativo, sem informação pessoal real. |
| `regiao` | Texto | Região brasileira associada ao cliente fictício. |
| `segmento` | Texto | Pequena empresa, média empresa ou pessoa física. |
| `produto_id` | Inteiro | Identificador do produto. |
| `produto` | Texto | Nome do produto demonstrativo. |
| `categoria` | Texto | Categoria do produto ou tipo de atendimento. |
| `canal` | Texto | Canal de venda ou recebimento do chamado. |
| `status` | Texto | Concluído/Cancelado para vendas; Resolvido/Aberto para atendimento. |
| `quantidade` | Inteiro | Quantidade de unidades do item; sempre positiva. |
| `preco_unitario_centavos` | Inteiro | Preço unitário em centavos de BRL, antes do desconto. |
| `desconto_pct` | Inteiro | Desconto percentual, de 0 a 100. |
| `receita_centavos` | Inteiro | Quantidade × preço unitário menos desconto, em centavos. Cálculo do item, inclusive cancelado. |
| `custo_centavos` | Inteiro | Custo total de mercadoria do item, em centavos. |
| `lucro_centavos` | Inteiro | Receita menos custo do item, em centavos. |
