-- Prazo só existe para pedido entregue e nunca é negativo.
select pedido_id, is_entregue, dias_entrega
from {{ ref('fct_pedidos') }}
where (is_entregue and (dias_entrega is null or dias_entrega < 0))
   or (not is_entregue and dias_entrega is not null)
