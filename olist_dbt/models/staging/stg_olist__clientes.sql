select
    customer_id                         as cliente_id,
    customer_state                      as estado,
    {{ title_case('customer_city') }}   as cidade
from {{ source('olist', 'customers') }}
