# Métricas e roteiros prontos para 5 ferramentas

Cada pasta traz as medidas na linguagem da ferramenta e o roteiro para montar o painel nela. O painel
publicado é a versão web; nas demais ferramentas, o painel é montado seguindo o roteiro.

As métricas são definidas uma vez em [`metricas/metricas.yml`](../metricas/metricas.yml) e cada ferramenta
recebe a tradução na própria linguagem. Todas leem a mesma fonte (`exports/pedidos_olist.csv`, gerado
pelo pipeline dbt) e têm que mostrar os números de [`metricas/valores_esperados.md`](../metricas/valores_esperados.md).

| Ferramenta | Pasta | O que essa versão destaca |
|---|---|---|
| Web (HTML/JS) | [`site/`](../site/) | Dashboard as code: dbt + CI + deploy automático |
| Power BI | [`powerbi/`](powerbi/) | Modelo estrela, DAX com `CALCULATE` e inteligência de tempo, drill-through |
| Tableau | [`tableau/`](tableau/) | LOD expressions, parâmetros, ações de painel |
| Metabase | [`metabase/`](metabase/) | SQL com filtros de campo, modelos, painel criado via API |
| Looker Studio | [`looker-studio/`](looker-studio/) | Campos calculados na fonte, comparação de período nativa, filtro cruzado |

## Layout comum
1. Filtros: período, estado, categoria
2. KPIs: receita, pedidos, ticket médio, nota média, prazo médio, % de entregas com atraso (com variação vs período anterior)
3. Receita por mês (alternando com pedidos, sem eixo duplo)
4. Mapa por estado
5. Top 10 categorias por receita
6. Nota média por faixa de prazo de entrega, com o contraste no prazo × atrasado
7. Tabela por estado

Os arquivos de medidas (`medidas.dax`, `campos_calculados.md`, `consultas.sql`) são gerados por
`scripts/gerar_pacotes_bi.py`. Os roteiros (`README.md` de cada pasta) foram escritos com a skill
[`traduzir-metricas-bi`](../.claude/skills/traduzir-metricas-bi/SKILL.md).
