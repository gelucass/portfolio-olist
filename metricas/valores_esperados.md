# Valores esperados

Gerado por `scripts/validar_metricas.py` a partir de `metricas/metricas.yml`. Não edite à mão.

Cada painel (Power BI, Tableau, Metabase, Looker Studio) tem que mostrar estes números nos mesmos recortes.

| Métrica | Total | Ano 2018 | Estado SP | Categoria Beleza saúde | SP em nov/2017 (Black Friday) |
|---|---:|---:|---:|---:|---:|
| Receita | R$ 15.786.203,57 | R$ 8.643.531,14 | R$ 5.904.881,86 | R$ 1.436.747,33 | R$ 411.642,89 |
| Pedidos | 98.353 | 53.774 | 41.264 | 8.758 | 2.971 |
| Ticket médio | R$ 160,51 | R$ 160,74 | R$ 143,10 | R$ 164,05 | R$ 138,55 |
| Nota média | 4,106 | 4,099 | 4,197 | 4,188 | 4,087 |
| Prazo médio de entrega (dias) | 12,074 | 11,689 | 8,274 | 11,588 | 10,225 |
| Entregas com atraso | 6,79% | 7,73% | 4,50% | 7,54% | 6,97% |
| Nota com entrega no prazo | 4,291 | 4,298 | 4,326 | 4,386 | 4,262 |
| Nota com entrega atrasada | 2,272 | 2,244 | 2,549 | 2,344 | 2,533 |
| Frete sobre produtos | 16,57% | 17,03% | 13,82% | 14,49% | 14,27% |

## Filtros de cada recorte

- **Total:** `true`
- **Ano 2018:** `data_compra >= '2018-01-01'`
- **Estado SP:** `estado = 'SP'`
- **Categoria Beleza saúde:** `categoria = 'Beleza saúde'`
- **SP em nov/2017 (Black Friday):** `estado = 'SP' and data_compra between '2017-11-01' and '2017-11-30'`
