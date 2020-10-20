"""Tests for behaviour of the column class."""

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import operator

import pytest
import prequel as pq


def test_escape():
    col = pq.Column('name"')
    assert str(col) == '"name"""'


def test_flatten():
    col = pq.Column("name")
    assert col.flatten() == ['"name"']


def test_as_value():
    col = pq.Column("name")
    assert col.as_value() == ['"name"']


def test_escape_table():
    col = pq.Column("val", table="table")
    assert str(col) == '"table"."val"'


def test_repr():
    col = pq.Column("col")
    assert repr(col) == "Column(table=None, column='col')"


def test_repr_table():
    col = pq.Column("col", table="table")
    assert repr(col) == "Column(table='table', column='col')" # TODO


def test_table():
    table = pq.Table("name")
    assert str(table) == '"name"'


def test_table_wrongtype():
    with pytest.raises(TypeError):
        pq.Table(0.1)


def test_table_col():
    col = pq.Table("hello").col("world")
    assert col == pq.Column(table=pq.Table("hello"), column="world")


def test_astable_str():
    table = pq.Table.as_table("hello")
    assert isinstance(table, pq.Table)
    assert table.table == "hello"


def test_astable_table():
    table_orig = pq.Table("hello")
    assert pq.Table.as_table(table_orig) is table_orig


def test_astable_wrongtype():
    with pytest.raises(TypeError):
        pq.Table.as_table(0.1)
