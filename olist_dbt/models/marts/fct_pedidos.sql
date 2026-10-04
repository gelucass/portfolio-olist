-- Uma linha por pedido: valores, entrega e avaliação.
-- Pedidos sem itens ficam de fora (inner join), assim como o período fora de data_inicio..data_fim.
with pedidos as (
    select *
    from {{ ref('stg_olist__pedidos') }}
    where comprado_em >= '{{ var("data_inicio") }}'
      and comprado_em <  '{{ var("data_fim") }}'
),

base as (
    select
        p.pedido_id,
        p.comprado_em,
        p.entregue_em,
        p.entrega_prevista_em,
        p.status_origem,
        s.status,
        c.estado,
        c.cidade,
        cat.categoria,
        i.qtd_itens,
        i.valor_produtos,
        i.valor_frete,
        a.nota_avaliacao,
        p.status_origem = 'delivered' and p.entregue_em is not null as is_entregue
    from pedidos as p
    inner join {{ ref('int_itens_agregados_por_pedido') }} as i using (pedido_id)
    inner join {{ ref('int_categoria_principal_por_pedido') }} as cat using (pedido_id)
    left join {{ ref('stg_olist__clientes') }} as c using (cliente_id)
    left join {{ ref('int_avaliacoes_por_pedido') }} as a using (pedido_id)
    left join {{ ref('status_pedido') }} as s using (status_origem)
)

select
    pedido_id,
    cast(comprado_em as date)                      as data_compra,
    date_trunc('month', comprado_em)::date         as mes_compra,
    coalesce(status, status_origem)                as status,
    estado,
    cidade,
    categoria,
    qtd_itens,
    valor_produtos,
    valor_frete,
    valor_produtos + valor_frete                   as valor_total,
    is_entregue,
    case when is_entregue
         then floor(epoch(entregue_em - comprado_em) / 86400)::integer end          as dias_entrega,
    case when is_entregue
         then cast(entregue_em as date) > cast(entrega_prevista_em as date) end     as is_atrasado,
    nota_avaliacao
from base
