# Looker Studio — particularidades

## Fonte de dados
- **Upload de arquivo** (CSV) é o mais rápido, mas fica estático. Para atualizar sem reenviar,
  use Google Sheets ou BigQuery como fonte.
- Na fonte, ajuste os tipos: `data_compra` Data (AAAAMMDD), `estado` como
  **Geo → Subdivisão do país (1º nível)**; se não reconhecer a sigla, crie `CONCAT("BR-", estado)`.
  `valor_*` como Moeda (BRL). Agregação padrão de `nota_avaliacao` e `dias_entrega`: Média.

## Campos calculados
- Crie os KPIs **na fonte de dados** (reutilizáveis em todos os gráficos), não no gráfico.
- Texto entre **aspas duplas** em `CASE WHEN entregue = "Sim"`.
- Campo agregado (`SUM(...) / SUM(...)`) não pode ser misturado com campo não agregado na mesma fórmula.
- Comparação com período anterior é nativa: em cada gráfico, "Período de comparação → Período anterior".

## Armadilhas que mudam o número
- `COUNT(pedido_id)` conta linhas; `COUNT_DISTINCT` conta pedidos. Iguais aqui, diferentes se o grão mudar.
- Gráfico com dois eixos: evite. Use um controle para alternar a métrica.
- O filtro cruzado precisa estar ativado em cada gráfico (Configuração → Interações → Filtro cruzado).

## Recursos que valem mostrar no portfólio
Controles de período/estado/categoria, filtro cruzado, parâmetros para trocar a métrica,
link público ("Qualquer pessoa com o link") e incorporação no site do portfólio.
