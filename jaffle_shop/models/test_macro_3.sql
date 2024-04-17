{% set a_relation = api.Relation.create(database='dbt', schema='prd', identifier='customers') %}
{% set b_relation = ref('customers') %}
{% set metrics = ['sum(number_of_orders)'] %}
{% set columns = ['last_name'] %}
with a as (

    select
    {% for column_name in columns %}
        {{ adapter.quote(column_name) }},
    {% endfor %}
    {% for metric in metrics %}
        {{ metric }} as "{{ loop.index0 }}_{{ metric }}",
          {% if not loop.last %}
            ,
          {% endif %}
    {% endfor %}
    from {{ a_relation }}
    group by
    {% for column_name in columns %}
        {{ adapter.quote(column_name) }}
        {% if not loop.last %}
          ,
        {% endif %}
    {% endfor %}


),

b as (

    select
    {% for column_name in columns %}
        {{ adapter.quote(column_name) }},
    {% endfor %}
    {% for metric in metrics %}
        {{ metric }} as "{{ loop.index0 }}_{{ metric }}",
          {% if not loop.last %}
            ,
          {% endif %}
    {% endfor %}
    from {{ b_relation }}
    group by
    {% for column_name in columns %}
        {{ adapter.quote(column_name) }}
        {% if not loop.last %}
          ,
        {% endif %}
    {% endfor %}

),

final as (

    select
    {% for column_name in columns %}
            COALESCE(a.{{ adapter.quote(column_name) }}, b.{{ adapter.quote(column_name) }}) as {{ adapter.quote(column_name) }},
    {% endfor %}
    {% for metric in metrics %}
             a."{{ loop.index0 }}_{{ metric }}" as "a_{{ metric }}",
             b."{{ loop.index0 }}_{{ metric }}" as "b_{{ metric }}",
            (a."{{ loop.index0 }}_{{ metric }}"  - b."{{ loop.index0 }}_{{ metric }}" )*100.0 / b."{{ loop.index0 }}_{{ metric }}" as "{{ metric }}_diff"
          {% if not loop.last %}
            ,
          {% endif %}
    {% endfor %}

    from a
    full outer join b on
    {% for column_name in columns %}
        a.{{ adapter.quote(column_name) }} = b.{{ adapter.quote(column_name) }}
        {% if not loop.last %}
          AND
        {% endif %}
    {% endfor %}

)

select * from final
