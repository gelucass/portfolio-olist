{# Equivalente ao str.title() do Python: maiúscula no início de cada palavra,
   inclusive depois de hífen e apóstrofo ("santa barbara d'oeste" -> "Santa Barbara D'Oeste"). #}
{% macro title_case(coluna) %}
    array_to_string(list_transform(string_split(lower({{ coluna }}), ' '),
        w -> array_to_string(list_transform(string_split(w, '-'),
            h -> array_to_string(list_transform(string_split(h, ''''),
                a -> upper(a[1]) || a[2:]), '''')), '-')), ' ')
{% endmacro %}
