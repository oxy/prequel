import prequel as pq


def test_column_convert():
    query = pq.Select("id")
    assert query.values == [pq.Column("id")]

def test_value_preserve():
    query = pq.Select(pq.Variable("hi"))
    assert query.values == [pq.Variable("hi")]

def test_flatten_plain():
    query = pq.Select(pq.Variable("hi"))
    assert query.flatten() == ["SELECT", pq.Variable("hi")]

def test_flatten():
    query = pq.Select("id").from_("user")
    assert query.flatten() == ["SELECT", '"id"', "FROM", '"user"']

