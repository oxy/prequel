# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
import prequel.utils as utils

@pytest.mark.parametrize(
    "name,expected",
    [('name"*!%_of_user', "name_of_user"), ("while", "_while"), ("1_name", "_1_name")],
)
def test_clean_ident(name, expected):
    assert utils.clean_ident(name) == expected
