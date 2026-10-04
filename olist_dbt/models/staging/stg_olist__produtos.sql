select
    product_id                                      as produto_id,
    coalesce(product_category_name, 'sem_categoria') as categoria_origem
from {{ source('olist', 'products') }}
