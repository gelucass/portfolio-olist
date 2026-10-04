-- Categoria principal do pedido = a de maior valor em produtos (desempate alfabético),
-- com o nome original ("cama_mesa_banho") convertido para leitura ("Cama mesa banho").
with valor_por_categoria as (
    select i.pedido_id, p.categoria_origem, sum(i.valor_produto) as valor
    from {{ ref('stg_olist__itens_pedido') }} as i
    left join {{ ref('stg_olist__produtos') }} as p using (produto_id)
    group by all
),

principal as (
    select pedido_id, coalesce(categoria_origem, 'sem_categoria') as categoria_origem
    from valor_por_categoria
    qualify row_number() over (partition by pedido_id order by valor desc, categoria_origem) = 1
),

palavras as (
    select pedido_id, categoria_origem,
           unnest(string_split(categoria_origem, '_')) as palavra,
           generate_subscripts(string_split(categoria_origem, '_'), 1) as posicao
    from principal
),

legivel as (
    select p.pedido_id, p.categoria_origem,
           string_agg(coalesce(a.com_acento, p.palavra), ' ' order by p.posicao) as nome
    from palavras as p
    left join {{ ref('palavras_acentuadas') }} as a on a.palavra = p.palavra
    group by all
)

select
    pedido_id,
    categoria_origem,
    upper(left(nome, 1)) || lower(substr(nome, 2)) as categoria
from legivel
