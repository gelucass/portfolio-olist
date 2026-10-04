---
name: traduzir-metricas-bi
description: Cria, altera ou traduz um KPI para Power BI (DAX), Tableau, Metabase e Looker Studio a partir de metricas/metricas.yml, gera os pacotes de cada ferramenta e o gabarito de valores esperados. Use ao adicionar ou mudar uma métrica, ao montar o painel numa nova ferramenta, ou quando pedirem "a mesma métrica no Power BI/Tableau/Metabase/Looker".
---

# Traduzir métricas para as ferramentas de BI

A regra do projeto: **uma métrica é definida uma vez** em `metricas/metricas.yml` e cada ferramenta recebe
uma tradução equivalente. Nunca crie a métrica direto numa ferramenta.

## Passo a passo

1. **Defina a métrica em SQL** (campo `sql`), sobre as colunas de `exports/pedidos_olist.csv`
   (a lista está no topo do YAML). Escreva também `rotulo`, `descricao` e `formato`
   (`moeda`, `inteiro`, `decimal` ou `percentual`).
2. **Traduza para cada ferramenta**, lendo antes a referência dela. Cada uma tem armadilhas próprias
   que mudam o resultado:
   - Power BI → `references/powerbi.md`
   - Tableau → `references/tableau.md`
   - Metabase → `references/metabase.md`
   - Looker Studio → `references/looker-studio.md`
3. **Confira a equivalência semântica**, não só a sintaxe:
   - Razões são sempre razão de somas (`SUM(a)/SUM(b)`), nunca média de razões por linha.
   - Nulos: SQL `avg` ignora nulos; confirme que a tradução também ignora (e não conta como zero).
   - Contagem de pedidos: a fonte tem 1 linha por pedido, então contar linhas e contar IDs distintos é igual.
     Se a fonte mudar de grão, use contagem distinta.
4. **Gere os artefatos e o gabarito:**
   ```bash
   .venv/bin/python scripts/validar_metricas.py    # falha se faltar alguma tradução
   .venv/bin/python scripts/gerar_pacotes_bi.py    # reescreve bi/<ferramenta>/medidas.*
   ```
5. **Mostre ao usuário** a métrica nova em `metricas/valores_esperados.md` e diga em qual visual de cada
   ferramenta ela entra. Se a métrica precisar de algo que uma ferramenta não faz de forma nativa
   (ex.: comparação com período anterior no Tableau), explique a alternativa usada.

## Ao montar o painel numa ferramenta nova

Siga o roteiro em `bi/<ferramenta>/README.md`. Se ele não existir, crie a partir da referência da
ferramenta, mantendo o mesmo layout do painel web (`site/index.html`): KPIs no topo, série mensal,
mapa por estado, top 10 categorias, nota × prazo de entrega e tabela por estado. Termine sempre com a
seção "Conferência", que aponta para `metricas/valores_esperados.md`.
