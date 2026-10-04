select
    order_id                              as pedido_id,
    cast(order_item_id as integer)        as item_seq,
    product_id                            as produto_id,
    cast(price as decimal(12, 2))         as valor_produto,
    cast(freight_value as decimal(12, 2)) as valor_frete
from {{ source('olist', 'order_items') }}
