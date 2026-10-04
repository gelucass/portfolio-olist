# E-commerce Olist · Vendas e Logística

Painel interativo com 98.353 pedidos da Olist (jan/2017 a ago/2018): vendas, geografia, categorias e o efeito do prazo de entrega na avaliação do cliente.

**[Abrir o painel](https://gelucass.github.io/portfolio-olist/)**

## Principais achados
- **R$ 15,8 mi** em receita, ticket médio de **R$ 160,51**.
- **SP** concentra 37% da receita, seguido de RJ e MG.
- **6,8%** das entregas chegam depois da data prometida.
- **Atraso derruba a avaliação:** nota média de **4,29** com entrega no prazo e **2,27** com atraso.

## Como funciona
| Etapa | Arquivo |
|---|---|
| Junta as tabelas brutas (pedidos, itens, produtos, clientes, avaliações) em 1 linha por pedido | `build_dataset.py` |
| Painel em HTML/JS puro, sem bibliotecas: filtros de período, estado e categoria, com filtro cruzado ao clicar no mapa, nas barras ou na tabela | `index.html` |

Os dados do painel ficam agregados por mês × estado × categoria dentro do próprio HTML. Por isso ele abre em qualquer navegador, sem servidor.

## Reproduzir
1. Baixe o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e extraia os CSVs em `raw/`.
2. `pip install pandas` e `python build_dataset.py` (gera `pedidos_olist.csv`).

Dados: Olist, licença CC BY-NC-SA 4.0.
