# Metabase

## 1. Subir o ambiente
Metabase + Postgres via Docker (o `docker-compose.yml` entra junto com o Airflow). A tabela `pedidos`
é carregada a partir de `exports/pedidos_olist.csv`. Em **Admin → Modelo de dados → pedidos**:
`estado` = Estado, `valor_*` = Moeda (BRL), `data_compra` = Data de criação.

## 2. Perguntas
- As perguntas SQL estão em [`consultas.sql`](consultas.sql), uma por bloco. Cada uma usa **filtros de campo**
  (`{{estado}}`, `{{periodo}}`, `{{categoria}}`), que precisam ser configurados como *Field Filter*
  apontando para a coluna certa, e não como texto.
- Mapa e top 10 categorias: use o **editor visual** (Resumir: Soma de valor_total; Agrupar por estado),
  para mostrar os dois modos de trabalho.
- Crie um **Modelo** `Pedidos` e, se a versão tiver, **Métricas** reutilizáveis para Receita e % Atraso.

## 3. Painel
| Bloco | Cartão |
|---|---|
| KPIs | Visualização **Tendência** (receita por mês) com comparação com o período anterior + números |
| Série mensal | Linha a partir de "Receita e pedidos por mês", mostrando uma série por vez |
| Mapa | Mapa de região, Brasil, por estado |
| Categorias | Barra horizontal, limite 10 |
| Nota × prazo | Barras a partir de "Nota média por prazo de entrega" |
| Tabela | Tabela agrupada por estado com formatação condicional em % atraso |

Ligue os três filtros do painel a **todos** os cartões e ative o filtro cruzado (clicar no mapa filtra o painel).

## 4. O que destacar no portfólio
- **Painel via API** (dashboard as code): o script que cria perguntas e painel entra junto com o Docker.
- Alertas ("avise se % atraso passar de 10%") e assinatura por e-mail.
- Filtros ligados: estado limitando as opções de cidade.

## 5. Conferência
Compare com [`valores_esperados.md`](../../metricas/valores_esperados.md). Atenção à divisão inteira do
Postgres: as consultas já usam `1.0 *` onde precisa. Divergiu? Use o agent `auditor-bi`.
