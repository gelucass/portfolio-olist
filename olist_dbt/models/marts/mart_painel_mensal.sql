-- Base do painel web: mês × estado × categoria, só com somas e contagens.
-- Médias e percentuais são calculados no navegador a partir delas, o que permite
-- refiltrar sem perder a ponderação correta.
with pedidos as (
    select
        *,
        case
            when dias_entrega <= 7  then 0
            when dias_entrega <= 14 then 1
            when dias_entrega <= 21 then 2
            when dias_entrega <= 30 then 3
            when dias_entrega is not null then 4
        end as faixa_prazo
    from {{ ref('fct_pedidos') }}
)

select
    mes_compra,
    estado,
    categoria,
    count(*)                                                     as pedidos,
    sum(valor_total)                                             as receita,
    sum(valor_frete)                                             as valor_frete,
    sum(valor_produtos)                                          as valor_produtos,
    count(*) filter (where is_entregue)                          as pedidos_entregues,
    count(*) filter (where is_atrasado)                          as pedidos_atrasados,
    count(*) filter (where status = 'Cancelado')                 as pedidos_cancelados,
    coalesce(sum(dias_entrega), 0)                               as soma_dias_entrega,
    count(dias_entrega)                                          as pedidos_com_prazo,
    coalesce(sum(nota_avaliacao), 0)                             as soma_notas,
    count(nota_avaliacao)                                        as pedidos_avaliados,
    {% for f in range(5) %}
    coalesce(sum(nota_avaliacao) filter (where faixa_prazo = {{ f }}), 0) as soma_nota_faixa_{{ f }},
    count(nota_avaliacao) filter (where faixa_prazo = {{ f }})            as avaliados_faixa_{{ f }},
    {% endfor %}
    coalesce(sum(nota_avaliacao) filter (where is_atrasado), 0)      as soma_nota_atrasados,
    count(nota_avaliacao) filter (where is_atrasado)                 as avaliados_atrasados,
    coalesce(sum(nota_avaliacao) filter (where not is_atrasado), 0)  as soma_nota_no_prazo,
    count(nota_avaliacao) filter (where not is_atrasado)             as avaliados_no_prazo
from pedidos
group by all
