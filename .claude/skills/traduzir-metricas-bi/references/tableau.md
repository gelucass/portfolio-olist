# Tableau — particularidades

## Fonte de dados
- Conecte em `exports/pedidos_olist.csv` (Arquivo de texto) e gere uma **extração**.
  O **Tableau Public** só publica com extração e torna os dados públicos: nunca use dados de empresa nele.
- Confira os tipos: `data_compra` como Data, `valor_*` e `nota_avaliacao` como Número (decimal),
  `estado` com papel geográfico **Estado/Província** (país Brasil).

## Campos calculados
- Cálculo **agregado** e de **linha** não se misturam na mesma expressão.
  `SUM([valor_total]) / COUNTD([pedido_id])` é válido; `[valor_total] / COUNTD([pedido_id])` não é.
- `IIF` e `IF ... THEN ... END` sem `ELSE` retornam NULL, e `AVG` ignora NULL: é isso que faz
  `AVG(IF [entrega_atrasada] = 'Não' THEN [nota_avaliacao] END)` equivaler ao `filter` do SQL.
- **LOD expressions** resolvem perguntas em outro grão. Exemplo, % da receita do estado no total:
  `SUM([valor_total]) / SUM({FIXED : SUM([valor_total])})`.
- Comparação com período anterior: cálculo de tabela
  `(ZN(SUM([valor_total])) - LOOKUP(ZN(SUM([valor_total])), -1)) / ABS(LOOKUP(ZN(SUM([valor_total])), -1))`,
  calculado ao longo de `MÊS(data_compra)`.

## Armadilhas que mudam o número
- Filtros de dimensão rodam **depois** de `FIXED`. Para o LOD respeitar o filtro, coloque o filtro
  no contexto (botão direito → Adicionar ao contexto).
- `COUNT([pedido_id])` conta linhas não nulas; use `COUNTD` se a fonte puder ter mais de uma linha por pedido.
- Mapa: estados sem papel geográfico aparecem como "desconhecidos" e somem do mapa.

## Recursos que valem mostrar no portfólio
Parâmetro para trocar a métrica do mapa (Receita/% atraso/Nota), ações de painel (filtro ao clicar
no mapa), tooltip com gráfico (viz in tooltip) e publicação no Tableau Public com link.
