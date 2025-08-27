from dbt_sentry.lineage import model


def test_lineage():
    m = model.Model(
        name="test",
        schema="test",
        database="test",
        query="select a, 1+c as b from table",
    )
    col = m.get_columns()
    assert len(col) == 2
    assert col[0] == "a"
    assert col[1] == "b"
