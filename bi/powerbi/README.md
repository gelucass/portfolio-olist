# Power BI

## 1. Fonte e modelo
1. **Obter dados → Texto/CSV** → `exports/pedidos_olist.csv` → **Transformar dados**.
2. Renomeie a consulta para `pedidos`. Em `valor_produtos`, `valor_frete`, `valor_total`, `dias_entrega` e
   `nota_avaliacao`: **Alterar tipo → Usando localidade → Número decimal / Inglês (Estados Unidos)**.
   Sem isso, o ponto decimal é lido como separador de milhar e os valores ficam 100× maiores.
3. `data_compra` como **Data**. Feche e aplique.
4. Crie a tabela `Calendario` (DAX no fim de [`medidas.dax`](medidas.dax)), marque como **tabela de datas**
   e relacione `Calendario[Data]` 1:* `pedidos[data_compra]`.
5. Crie uma tabela vazia `_Medidas` (Inserir dados → OK) e cole as medidas de [`medidas.dax`](medidas.dax),
   com o formato indicado em cada comentário.

## 2. Visuais
| Bloco | Visual | Campos |
|---|---|---|
| Filtros | Segmentação | `Calendario[Data]` (entre), `pedidos[estado]`, `pedidos[categoria]` (lista suspensa) |
| KPIs | Cartão (novo) | Uma medida por cartão; em Receita, valor de referência = `Var. receita vs mês anterior` |
| Série mensal | Gráfico de linhas | Eixo `Calendario[Ano-Mês]`; valores via **parâmetro de campo** com `[Receita]` e `[Pedidos]` |
| Mapa | Mapa coroplético | Local `pedidos[estado]` (categoria de dados: Estado ou Província), saturação `[Receita]` |
| Categorias | Barras horizontais | `pedidos[categoria]`, `[Receita]`, filtro Top N = 10 por `[Receita]` |
| Nota × prazo | Colunas | Coluna calculada de faixa de prazo (abaixo) × `[Nota média]`; cartões `[Nota no prazo]` e `[Nota com atraso]` |
| Tabela | Matriz | `pedidos[estado]`, `[Pedidos]`, `[Receita]`, `[Ticket médio]`, `[Prazo médio]`, `[% Atraso]` (barras de dados), `[Nota média]` |

```
Faixa de prazo =
SWITCH ( TRUE (),
    ISBLANK ( pedidos[dias_entrega] ), BLANK (),
    pedidos[dias_entrega] <= 7, "1. até 7 dias",
    pedidos[dias_entrega] <= 14, "2. 8 a 14",
    pedidos[dias_entrega] <= 21, "3. 15 a 21",
    pedidos[dias_entrega] <= 30, "4. 22 a 30",
    "5. mais de 30" )
```

## 3. O que destacar no portfólio
- **Parâmetro de campo** para alternar Receita/Pedidos no mesmo gráfico, sem eixo duplo.
- **Drill-through**: página "Detalhe do estado" com `pedidos[estado]` como campo de drill-through
  (cidades, categorias e evolução do estado).
- **Dica de ferramenta de página** no mapa, com o mini-resumo do estado.
- Medidas em pastas de exibição (KPIs, Logística, Avaliação) na tabela `_Medidas`.

## 4. Publicação
Power BI Desktop roda só no Windows. Para o portfólio: **Publicar na Web** (exige licença Pro e a opção
liberada pelo administrador) ou exporte PDF e grave um GIF da navegação. Salve como **.pbip** (projeto do
Power BI) para versionar o modelo em texto no Git.

## 5. Conferência
Aplique cada recorte de [`valores_esperados.md`](../../metricas/valores_esperados.md) nas segmentações e
compare os cartões. Divergiu? Peça ao agent `auditor-bi`, informando ferramenta, recorte e valor.
