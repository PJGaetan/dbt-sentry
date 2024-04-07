PROFILE_QUERY = """
{{ dbt_profiler.get_profile(relation=ref("PLACEHOLDER_MODEL_NAME")) }}
"""

COMPARE_COLUMNS_QUERY = """
{{ 
  audit_helper.compare_all_columns(
    a_relation=ref('PLACEHOLDER_MODEL_NAME'),
    b_relation=api.Relation.create(database='dbt', schema='main', identifier='test_2'),
    exclude_columns=[EXCLUDED_COLUMNS],
    primary_key='customer_id'
  ) 
}}
"""

COLUMNS_PROFILE_QUERY = """
{{ audit_helper.compare_relation_columns(
    a_relation=api.Relation.create(database='dbt', schema='main', identifier='test_2'),
    b_relation=ref('PLACEHOLDER_MODEL_NAME'),
) }}
"""

COMPARE_RELATION_QUERY = """
{{ audit_helper.compare_relations(
    a_relation=api.Relation.create(database='dbt', schema='main', identifier='test_2'),
    b_relation=ref('PLACEHOLDER_MODEL_NAME'),
    exclude_columns=[EXCLUDED_COLUMNS],
    summarize=false,
    primary_key="customer_id"
) }}
"""
