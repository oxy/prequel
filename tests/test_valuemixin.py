# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from typing import Any

import prequel as pq
import operator

import pytest

class ValueMixinTest(pq.ValueMixin, pq.types.Value):
    def __init__(self, value: Any):
        self.val = value

    def flatten(self):
        return [str(self.val)]

    def as_value(self):
        return [str(self.val)]

    def boolean(self):
        return False


@pytest.mark.parametrize("op,expected", [
    (g := operator.attrgetter(x), g(operator), g(pq.Operator))[1:] for x in ['eq', 'ne', 'le', 'lt', 'ge', 'gt']
])
def test_boolops(op, expected):
    res = op(ValueMixinTest("a"), ValueMixinTest("b"))
    assert isinstance(res, pq.Expression)
    assert res.op == expected
    assert res.lhs == ValueMixinTest("a")
    assert res.rhs == ValueMixinTest("b")
    

def test_like():
    res = ValueMixinTest("a").like(ValueMixinTest("b"))
    assert isinstance(res, pq.Expression)
    assert res.lhs == ValueMixinTest("a")
    assert res.op == pq.Operator.like
    assert res.rhs == ValueMixinTest("b")


def test_between():
    res = ValueMixinTest("a").between(ValueMixinTest("b"), ValueMixinTest("c"))
    assert isinstance(res, pq.Between)
    assert res.val == ValueMixinTest("a")
    assert res.min == ValueMixinTest("b")
    assert res.max == ValueMixinTest("c")
