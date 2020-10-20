# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import inspect
import pytest

import prequel as pq


def test_mkquery_var_nodefault():
    res = pq.mkquery([pq.Variable("name")])
    assert str(inspect.signature(res)) == "(name) -> Tuple[str, Any]"
    assert res(None) == ("$1", None)


def test_mkquery_var_nulldefault():
    res = pq.mkquery([pq.Variable("id", None)])
    assert str(inspect.signature(res)) == "(id=None) -> Tuple[str, Any]"
    assert res() == ("$1", None)


def test_mkquery_var_typedefault():
    res = pq.mkquery([pq.Variable("id", int)])
    assert str(inspect.signature(res)) == "(id: int) -> Tuple[str, int]"
    assert res(None) == ("$1", None)


def test_mkquery_var_default():
    res = pq.mkquery([pq.Variable("id", 101)])
    assert str(inspect.signature(res)) == "(id: int = 101) -> Tuple[str, int]"
    assert res() == ("$1", 101)


def test_mkquery_var_repeat():
    var = pq.Variable("name")
    res = pq.mkquery([var, var])
    assert str(inspect.signature(res)) == "(name) -> Tuple[str, Any]"
    assert res(None) == ("$1 $1", None)


def test_mkquery_str():
    res = pq.mkquery(["string"])
    assert str(inspect.signature(res)) == "() -> Tuple[str]"
    assert res() == ("string",)


def test_mkquery_comma():
    res = pq.mkquery(["one", ",", "two"])
    assert str(inspect.signature(res)) == "() -> Tuple[str]"
    assert res() == ("one, two",)


def test_mkquery_bracket():
    res = pq.mkquery(["(", "one", "=", "two", ")"])
    assert str(inspect.signature(res)) == "() -> Tuple[str]"
    assert res() == ("(one = two)",)
