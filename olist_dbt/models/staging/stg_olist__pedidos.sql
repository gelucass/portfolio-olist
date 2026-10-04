select
    order_id                                         as pedido_id,
    customer_id                                      as cliente_id,
    order_status                                     as status_origem,
    cast(order_purchase_timestamp as timestamp)      as comprado_em,
    cast(order_delivered_customer_date as timestamp) as entregue_em,
    cast(order_estimated_delivery_date as timestamp) as entrega_prevista_em
from {{ source('olist', 'orders') }}
