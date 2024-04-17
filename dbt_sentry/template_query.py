PROFILE_QUERY = """
{{ dbt_profiler.get_profile(relation=ref("PLACEHOLDER_MODEL_NAME")) }}
"""

COMPARE_COLUMNS_QUERY = """
{{ 
  audit_helper.compare_all_columns(
    a_relation=ref('PLACEHOLDER_MODEL_NAME'),
    b_relation=RELATION_TO_REPLACE,
    exclude_columns=[EXCLUDED_COLUMNS],
    primary_key='customer_id'
  ) 
}}
"""

COLUMNS_PROFILE_QUERY = """
{{ audit_helper.compare_relation_columns(
    a_relation=RELATION_TO_REPLACE,
    b_relation=ref('PLACEHOLDER_MODEL_NAME'),
) }}
"""

COMPARE_RELATION_QUERY = """
{{ audit_helper.compare_relations(
    a_relation=RELATION_TO_REPLACE,
    b_relation=ref('PLACEHOLDER_MODEL_NAME'),
    exclude_columns=[EXCLUDED_COLUMNS],
    summarize=false,
    primary_key="customer_id"
) }}
"""

COMPARE_METRICS_QUERY = """
{{ compare_columns_metrics(
    a_relation=RELATION_TO_REPLACE,
    b_relation=ref('PLACEHOLDER_MODEL_NAME'),
    columns=[COLUMNS_TO_REPLACE],
    metrics=[METRICS_TO_REPLACE],
) }}
"""

TEMPLATED_METRICS_JINJA_QUERY = """
{% set a_relation = RELATION_TO_REPLACE %}
{% set b_relation = ref('PLACEHOLDER_MODEL_NAME') %}
{% set metrics = [METRICS_TO_REPLACE] %}
{% set columns = [COLUMNS_TO_REPLACE] %}
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
"""
