# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
import prequel as pq


@pytest.mark.parametrize("name", ["while", "1take", "a-b", "i>1", "oxy's"])
def test_bad_variable_name(name):
    with pytest.raises(ValueError):
        var = pq.Variable(name)


def test_repr_nodefault():
    var = pq.Variable("name", ...)
    assert repr(var) == "Variable('name')"


def test_repr_default():
    var = pq.Variable("name", "value")
    assert repr(var) == "Variable('name', 'value')"


def test_var_flatten():
    var = pq.Variable("name", "value")
    assert var.flatten() == [var]


def test_var_as_value():
    var = pq.Variable("name", "value")
    assert var.as_value() == [var]
