{# Teste genérico: a combinação de colunas é única. #}
{% test combinacao_unica(model, columns) %}
select {{ columns | join(', ') }}, count(*) as ocorrencias
from {{ model }}
group by {{ columns | join(', ') }}
having count(*) > 1
{% endtest %}
