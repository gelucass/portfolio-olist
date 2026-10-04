# Tableau

## 1. Fonte
1. **Conectar → Arquivo de texto** → `exports/pedidos_olist.csv`. Mude para **Extração**.
2. Tipos: `data_compra` Data; `valor_*`, `dias_entrega`, `nota_avaliacao` Número (decimal);
   `estado` → **Função geográfica → Estado/Província** (em Mapa → Editar locais, país Brasil).
3. Crie os campos de [`campos_calculados.md`](campos_calculados.md).

## 2. Planilhas e painel
| Planilha | Construção |
|---|---|
| KPIs | Nomes de medidas / Valores de medidas em texto, ou uma planilha por KPI com o número grande |
| Série mensal | `MÊS(data_compra)` contínuo em Colunas; o parâmetro **Métrica** (Receita/Pedidos) em Linhas via campo `CASE [Métrica] WHEN 'Receita' THEN [Receita] ELSE [Pedidos] END` |
| Mapa | `estado` em Detalhe, campo do parâmetro **Métrica do mapa** (Receita/% atraso/Nota) em Cor |
| Categorias | `categoria` em Linhas, `[Receita]` em Colunas, filtro **Superior 10 por Receita** |
| Nota × prazo | Campo de faixa de prazo (abaixo) em Colunas, `[Nota média]` em Linhas |
| Tabela | `estado` em Linhas, Nomes de medidas em Colunas, formatação de destaque em `% Atraso` |

```
// Faixa de prazo
IF ISNULL([dias_entrega]) THEN NULL
ELSEIF [dias_entrega] <= 7 THEN '1. até 7 dias'
ELSEIF [dias_entrega] <= 14 THEN '2. 8 a 14'
ELSEIF [dias_entrega] <= 21 THEN '3. 15 a 21'
ELSEIF [dias_entrega] <= 30 THEN '4. 22 a 30'
ELSE '5. mais de 30' END
```

No painel: filtros de período, estado e categoria **aplicados a todas as planilhas que usam esta fonte**,
e **Ação de filtro** ao clicar no mapa e nas categorias.

## 3. O que destacar no portfólio
- **LOD**: participação do estado na receita total, `SUM([valor_total]) / SUM({FIXED : SUM([valor_total])})`.
  Adicione os filtros ao contexto para o LOD respeitá-los.
- **Parâmetros** trocando a métrica do mapa e da série.
- **Viz in tooltip**: ao passar no estado, a evolução mensal dele.
- Variação mensal com cálculo de tabela (`LOOKUP`), descrita na referência da skill.

## 4. Publicação
**Tableau Public** (gratuito, roda no Mac): Arquivo → Salvar no Tableau Public. O link vai para o
site do portfólio. Os dados ficam públicos: só use bases públicas como esta.

## 5. Conferência
Aplique os recortes de [`valores_esperados.md`](../../metricas/valores_esperados.md) e compare.
Divergiu? Use o agent `auditor-bi`.
