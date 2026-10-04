-- Agrega os itens antes de juntar com pedidos, para não duplicar linhas.
select
    pedido_id,
    count(*)           as qtd_itens,
    sum(valor_produto) as valor_produtos,
    sum(valor_frete)   as valor_frete
from {{ ref('stg_olist__itens_pedido') }}
group by pedido_id
