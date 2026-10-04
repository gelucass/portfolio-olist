# Looker Studio

## 1. Fonte
1. **Criar → Fonte de dados → Upload de arquivo** → `exports/pedidos_olist.csv`.
2. Tipos: `data_compra` Data (AAAAMMDD); `estado` **Geo → Subdivisão do país (1º nível)**
   (se não reconhecer, crie `CONCAT("BR-", estado)` com esse tipo); `valor_*` Moeda (BRL);
   agregação padrão de `nota_avaliacao` e `dias_entrega` = Média.
3. Adicione os campos de [`campos_calculados.md`](campos_calculados.md) **na fonte**, não nos gráficos.

## 2. Relatório
| Bloco | Componente |
|---|---|
| Filtros | Controle de período (`data_compra`), listas suspensas de `estado` e `categoria` |
| KPIs | Cartões de resultado, com **Período de comparação → Período anterior** |
| Série mensal | Série temporal por Ano-mês; métrica alternada com **parâmetro** (Receita/Pedidos) |
| Mapa | Mapa preenchido, `estado` × Receita |
| Categorias | Barras, `categoria` × Receita, 10 barras |
| Nota × prazo | Barras com dimensão de faixa de prazo (CASE abaixo) × Nota média |
| Tabela | Tabela por `estado` com barras em % atraso |

```
CASE
  WHEN dias_entrega IS NULL THEN NULL
  WHEN dias_entrega <= 7 THEN "1. até 7 dias"
  WHEN dias_entrega <= 14 THEN "2. 8 a 14"
  WHEN dias_entrega <= 21 THEN "3. 15 a 21"
  WHEN dias_entrega <= 30 THEN "4. 22 a 30"
  ELSE "5. mais de 30"
END
```

Ative **Filtro cruzado** em mapa, categorias e tabela.

## 3. O que destacar no portfólio
- Comparação com período anterior nativa nos cartões.
- Parâmetro trocando a métrica, sem eixo duplo.
- Para atualização automática, troque o upload por Google Sheets ou BigQuery alimentado pelo pipeline.

## 4. Publicação
Compartilhar → **Qualquer pessoa com o link pode ver**. Use também Arquivo → Incorporar relatório
para colocar no site do portfólio.

## 5. Conferência
Compare com [`valores_esperados.md`](../../metricas/valores_esperados.md). Divergiu? Use o agent `auditor-bi`.
