{{ compare_columns_metrics(
    a_relation=ref('stg_customers'),
    b_relation=api.Relation.create(database='dbt', schema='main', identifier='test_2'),
    columns=["last_name"],
    metrics=["count(*)"]
) }}
