{% set old_fct_orders_query %}
  select
        last_name,
	count(first_name) as cnt
    from {{ ref('stg_customers') }} 
    group by last_name
{% endset %}

{% set new_fct_orders_query %}
    select
        last_name,
	count(first_name) as cnt
    from "dbt"."main"."stg_customers"
    group by last_name
{% endset %}

{{ compare_columns_metrics(
    a_query=old_fct_orders_query,
    b_query=new_fct_orders_query,
    columns=["last_name"],
    metrics=["cnt"]
) }}
