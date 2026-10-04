-- O painel tem que somar exatamente o mesmo que a tabela de pedidos.
with painel as (
    select sum(pedidos) as pedidos, sum(receita) as receita, sum(pedidos_atrasados) as atrasados
    from {{ ref('mart_painel_mensal') }}
),
pedidos as (
    select count(*) as pedidos, sum(valor_total) as receita, count(*) filter (where is_atrasado) as atrasados
    from {{ ref('fct_pedidos') }}
)
select *
from painel, pedidos
where painel.pedidos <> pedidos.pedidos
   or abs(painel.receita - pedidos.receita) > 0.01
   or painel.atrasados <> pedidos.atrasados
