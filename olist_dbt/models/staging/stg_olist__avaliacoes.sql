select
    review_id                          as avaliacao_id,
    order_id                           as pedido_id,
    cast(review_score as integer)      as nota
from {{ source('olist', 'order_reviews') }}
