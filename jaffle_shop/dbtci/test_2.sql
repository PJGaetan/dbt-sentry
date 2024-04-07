{% set old_fct_orders_query %}
  select
	customer_id,
        last_name,
	first_name
    from {{ ref('stg_customers') }} 
{% endset %}

{% set new_fct_orders_query %}
    select
	customer_id,
        last_name,
	first_name
    from "dbt"."main"."stg_customers"
{% endset %}

{% if execute %}
{% set audit_query = audit_helper.compare_column_values(
    a_query=old_fct_orders_query,
    b_query=new_fct_orders_query,
    primary_key="customer_id",
    column_to_compare="last_name"
) %}
{% set audit_results = run_query(audit_query) %}
{#{% do audit_results.to_csv('/tmp/audit_results.csv') %}#}
{% endif %}
