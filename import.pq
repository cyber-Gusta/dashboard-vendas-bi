// Substitua o caminho abaixo pelo caminho local do CSV.
let
    Caminho = "C:\Dados\vendas.csv",
    Fonte = Csv.Document(File.Contents(Caminho), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars=true]),
    VaziosComoNull = Table.ReplaceValue(Cabecalhos, "", null, Replacer.ReplaceValue, Table.ColumnNames(Cabecalhos)),
    Tipos = Table.TransformColumnTypes(VaziosComoNull, {
        {"data", type date},
    {"item_id", Int64.Type},
    {"pedido_id", Int64.Type},
    {"cliente_id", Int64.Type},
    {"produto_id", Int64.Type},
    {"quantidade", Int64.Type},
    {"preco_unitario_centavos", Int64.Type},
    {"desconto_pct", Int64.Type},
    {"receita_centavos", Int64.Type},
    {"custo_centavos", Int64.Type},
    {"lucro_centavos", Int64.Type}
    }, "en-US")
in
    Tipos
