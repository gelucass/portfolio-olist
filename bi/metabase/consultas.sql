-- Gerado por scripts/gerar_pacotes_bi.py a partir de metricas/metricas.yml. Não edite à mão.
-- Cada bloco é uma pergunta SQL nativa sobre a tabela pedidos (Postgres).
-- Variáveis: {{estado}} = Filtro de campo -> pedidos.estado; {{periodo}} = Filtro de campo -> pedidos.data_compra;
--            {{categoria}} = Filtro de campo -> pedidos.categoria. Ligue as três aos filtros do painel.
-- Os colchetes [[ ]] tornam cada filtro opcional.

-- Pergunta: Receita (Valor dos produtos + frete.)
select sum(valor_total) as "Receita"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Pedidos (Quantidade de pedidos (uma linha por pedido na fonte).)
select count(*) as "Pedidos"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Ticket médio (Receita ÷ pedidos. É uma razão de somas, não a média de uma coluna.)
select sum(valor_total) / count(*) as "Ticket médio"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Nota média (Média da avaliação do cliente (1 a 5). Pedidos sem avaliação ficam fora da média.)
select avg(nota_avaliacao) as "Nota média"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Prazo médio de entrega (dias) (Dias entre a compra e a entrega, só para pedidos entregues.)
select avg(dias_entrega) as "Prazo médio de entrega (dias)"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Entregas com atraso (Pedidos entregues depois da data prometida ÷ pedidos entregues.)
select 1.0 * count(case when entrega_atrasada = 'Sim' then 1 end) / nullif(count(case when entregue = 'Sim' then 1 end), 0) as "Entregas com atraso"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Nota com entrega no prazo (Nota média dos pedidos entregues dentro do prazo.)
select avg(case when entrega_atrasada = 'Não' then nota_avaliacao end) as "Nota com entrega no prazo"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Nota com entrega atrasada (Nota média dos pedidos entregues depois do prazo.)
select avg(case when entrega_atrasada = 'Sim' then nota_avaliacao end) as "Nota com entrega atrasada"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Frete sobre produtos (Quanto o frete representa sobre o valor dos produtos.)
select sum(valor_frete) / sum(valor_produtos) as "Frete sobre produtos"
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]];

-- Pergunta: Receita e pedidos por mês (gráfico de linha)
select date_trunc('month', data_compra)::date as mes,
       sum(valor_total) as receita,
       count(*) as pedidos
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]]
group by 1
order by 1;

-- Pergunta: Nota média por prazo de entrega
select case when dias_entrega <= 7 then '1. até 7 dias'
            when dias_entrega <= 14 then '2. 8 a 14'
            when dias_entrega <= 21 then '3. 15 a 21'
            when dias_entrega <= 30 then '4. 22 a 30'
            else '5. mais de 30' end as faixa_prazo,
       avg(nota_avaliacao) as nota_media,
       count(nota_avaliacao) as pedidos_avaliados
from pedidos
where true
  [[and {{estado}}]]
  [[and {{periodo}}]]
  [[and {{categoria}}]]
  and dias_entrega is not null
group by 1
order by 1;
