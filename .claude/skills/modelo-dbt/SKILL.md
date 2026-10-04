---
name: modelo-dbt
description: Cria ou altera um modelo dbt no padrão do projeto (camadas, nomes em português, testes e documentação) e valida com dbt build. Use ao pedir um modelo, tabela, mart, staging ou dimensão nova, ou ao mudar a lógica de um modelo existente.
---

# Criar ou alterar um modelo dbt

## 1. Escolha a camada pelo papel do modelo
| Camada | Prefixo | Faz | Não faz |
|---|---|---|---|
| staging | `stg_<fonte>__<entidade>` | 1:1 com a fonte: tipagem, renomear para português, `coalesce` simples | join, agregação |
| intermediate | `int_<o_que_faz>` | Leva para o grão de destino (ex.: agregar itens por pedido) | regras de exibição |
| marts | `fct_` / `dim_` / `mart_` | Tabelas consumidas pelo BI e pelo painel | lógica que outra camada já resolve |

## 2. Escreva o SQL
- Declare o **grão** num comentário na primeira linha (`-- Uma linha por pedido.`).
- **Agregue antes de juntar.** Join de pedido com item sem agregar duplica valores do pedido.
- Desempates com `qualify row_number() over (...)` precisam de critério determinístico.
- Datas de corte vêm de `var('data_inicio')` / `var('data_fim')`, nunca fixas no SQL.
- Siga o estilo dos modelos vizinhos: CTEs nomeadas pelo que contêm, `using` quando a chave tem o mesmo nome.

## 3. Documente e teste no YAML da camada
- `description` do modelo e das colunas que não são óbvias.
- Chave do grão: `unique` + `not_null` (ou o teste genérico `combinacao_unica` para chave composta).
- Colunas categóricas: `accepted_values`. Chaves estrangeiras: `relationships`.
- Regra de negócio importante: teste singular em `olist_dbt/tests/assert_<regra>.sql`, que retorna as linhas que violam a regra.
- Parâmetros de teste genérico ficam dentro de `arguments:` (dbt 1.10+).

## 4. Valide
```bash
cd olist_dbt && ../.venv/bin/dbt build --select +<modelo>+ --profiles-dir .
```
Se o modelo alimenta `fct_pedidos` ou `mart_painel_mensal`, rode também `scripts/exportar.py` e
`scripts/validar_metricas.py`, e diga ao usuário se algum valor em `metricas/valores_esperados.md` mudou.

## 5. Revise
Peça ao agent `revisor-dbt` para revisar a mudança antes do commit.
