import pytest
import prequel as pq


def test_insert_init():
    query = pq.Insert("table", ["column1", pq.Column("column2")])
    assert isinstance(query.table, pq.Table)
    assert query.table.table == "table"
    assert query.columns == [pq.Column("column1"), pq.Column("column2")]


def test_insert_values_fromquery_len():
    query = pq.Insert("table", ["column1", "column2"])
    select = pq.Select("col1", "col2").from_("table2")
    query.values_fromquery(select)

    assert query._values == select.flatten()  # pylint: disable=protected-access

def test_insert_values_fromquery_nonmatch():
    query = pq.Insert("table", ["column1", "column2"])
    select = pq.Select("col1").from_("table2")
    with pytest.raises(ValueError):
        query.values_fromquery(select)


def test_insert_values():
    query = pq.Insert("table", ["column1", "column2"])

