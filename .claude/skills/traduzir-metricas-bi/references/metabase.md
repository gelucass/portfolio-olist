# Metabase — particularidades

## Fonte de dados
- O Metabase lê de um banco, não de arquivo. No portfólio, um Postgres no Docker recebe
  `exports/pedidos_olist.csv` na tabela `pedidos` (ver `bi/metabase/`).
- Em Admin → Modelo de dados, defina os tipos semânticos: `estado` como **Estado**,
  `valor_*` como **Moeda (BRL)**, `data_compra` como **Data de criação**.

## Perguntas
- **Editor visual** para o simples (Receita por mês) e **SQL nativo** quando a métrica tem filtro
  condicional (% atraso, nota no prazo). As expressões em `metricas.yml` são SQL de Postgres.
- Para os filtros do painel funcionarem numa pergunta SQL, use **filtro de campo** (variável do tipo
  "Field Filter"), e não variável de texto:
  ```sql
  select sum(valor_total) as receita from pedidos where {{estado}} and {{periodo}}
  ```
  Ligue a variável `estado` ao campo `pedidos.estado` e `periodo` a `pedidos.data_compra`.
- Crie um **Modelo** (`pedidos` limpo) e, nas versões com o recurso, **Métricas** reutilizáveis,
  para que outras perguntas não redefinam o KPI.

## Armadilhas que mudam o número
- Divisão inteira no Postgres: `count(...) / count(...)` dá 0. Multiplique por `1.0` ou faça cast.
- Cada cartão precisa estar ligado ao filtro do painel; um cartão esquecido mostra o total sem aviso.
- Fuso horário do relatório (Admin → Localização) pode deslocar datas na virada do mês.

## Recursos que valem mostrar no portfólio
Cartão de tendência com "comparar com período anterior", filtros ligados (estado → cidade),
clique no gráfico para filtrar o painel (cross-filter), alertas e assinatura por e-mail, e a criação
do painel via API (dashboard as code).
