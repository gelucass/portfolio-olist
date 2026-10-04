-- Alguns pedidos têm mais de uma avaliação: usa a média.
select
    pedido_id,
    round(avg(nota), 1) as nota_avaliacao
from {{ ref('stg_olist__avaliacoes') }}
group by pedido_id
