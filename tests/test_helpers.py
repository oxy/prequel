import pytest
import prequel as pq


def test_group_solo():
    res = pq.group([pq.Variable("a")], pq.Operator.and_)
    assert res == pq.Variable("a")


def test_group_multi():
    res = pq.group(
        [pq.Variable("a"), pq.Variable("b"), pq.Variable("c")],
        pq.Operator.add
    )
    assert res == pq.Expression(
            pq.Expression(
                pq.Variable("a"), pq.Operator.add, pq.Variable("b")
            ),
            pq.Operator.add,
            pq.Variable("c")
    )


def test_group_none():
    with pytest.raises(ValueError):
        res = pq.group([], pq.Operator.add)
