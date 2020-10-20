# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import prequel as pq

def test_commasep_flatten_str():
    block = pq.CommaSeparated("hi", "hello")
    assert block.flatten() == ["hi", ",", "hello"]


def test_commasep_flatten_value():
    block = pq.CommaSeparated(pq.Variable("a"), pq.Variable("b"))
    assert block.flatten() == [pq.Variable("a"), ",", pq.Variable("b")]
