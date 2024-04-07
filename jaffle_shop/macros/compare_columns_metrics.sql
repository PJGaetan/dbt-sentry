{% macro compare_columns_metrics(a_query, b_query, columns=[], metrics=[]) -%}
    {{ return(adapter.dispatch('compare_columns_metrics')(a_query, b_query, columns, metrics)) }}
{%- endmacro %}

{% macro default__compare_columns_metrics(a_query, b_query, columns=[], metrics=[]) %}
    
    
with a as (

    {{ a_query }}

),

b as (

    {{ b_query }}

),

final as (

    select
    {% for column_name in columns %} 
	    a.{{ adapter.quote(column_name) }}, 
    {% endfor %}
    {% for metric in metrics %} 
         a.{{ metric }} as a_{{ metric }},
	 b.{{ metric }} as b_{{ metric }},
	(a_{{ metric }} - b_{{ metric }})*100.0 / b_{{ metric }} as {{ metric }}_diff
      {% if not loop.last %}
        , 
      {% endif %} 
    {% endfor %}

    from a
    inner join b on
    {% for column_name in columns %} 
        a.{{ adapter.quote(column_name) }} = b.{{ adapter.quote(column_name) }}
    {% if not loop.last %}
      AND 
    {% endif %} 
{% endfor %}


)

select * from final
{% endmacro %}
