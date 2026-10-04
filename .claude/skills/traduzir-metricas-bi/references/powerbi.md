# Power BI — particularidades

## Modelo
- Monte um **modelo estrela**: fato `pedidos` + dimensão de calendário (`Calendario`), marcada como
  **tabela de datas** (Modelagem → Marcar como tabela de data). Sem ela, a inteligência de tempo
  (`DATEADD`, `SAMEPERIODLASTYEAR`) não funciona direito.
- Relacione `Calendario[Data]` 1:* `pedidos[data_compra]`, filtro em uma direção.
- Desative medidas implícitas (Arquivo → Opções → Relatório) para forçar o uso das medidas DAX.

## DAX
- Use `DIVIDE(a, b)` em vez de `a / b`: retorna BLANK em divisão por zero.
- `CALCULATE` troca o contexto de filtro. `CALCULATE([Pedidos], pedidos[entregue] = "Sim")` é o
  equivalente a `count(*) filter (where entregue = 'Sim')`.
- `AVERAGE` ignora BLANK, como o `avg` do SQL. Células vazias do CSV viram BLANK desde que a coluna
  esteja tipada como número.
- Comparação com período anterior:
  ```
  Receita mês anterior = CALCULATE ( [Receita], DATEADD ( Calendario[Data], -1, MONTH ) )
  Var. receita % = DIVIDE ( [Receita] - [Receita mês anterior], [Receita mês anterior] )
  ```
- Organize as medidas numa tabela vazia `_Medidas` com pastas de exibição (KPIs, Logística, Avaliação).

## Armadilhas que mudam o número
- **Localidade na importação do CSV:** o arquivo usa ponto como decimal. No Power Query, em
  "Alterar tipo → Usando localidade", escolha **Inglês (Estados Unidos)** para `valor_*`,
  `dias_entrega` e `nota_avaliacao`. Com localidade pt-BR, `160.51` vira `16051`.
- `data_compra` deve ser **Data**, não Data/Hora, para o relacionamento com o calendário bater.
- Formatos: moeda com `R$ #,##0.00`, percentual com `0.0%`.

## Recursos que valem mostrar no portfólio
Drill-through de estado para uma página de detalhe, tooltip de página, formatação condicional na
tabela, bookmarks para alternar Receita/Pedidos, e "Publicar na Web" (exige licença) ou PDF + GIF.
