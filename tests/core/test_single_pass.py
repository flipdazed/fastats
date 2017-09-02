
import math

import numpy as np
from pytest import approx, raises

from fastats import single_pass


def twice(x):
    return x * 2


def test_basic_sanity():
    data = np.arange(10)

    assert data[0] == 0
    assert data[1] == 1
    assert data[-1] == 9

    no_kwargs = single_pass(data)

    assert no_kwargs[0] == 0
    assert no_kwargs[1] == 1
    assert no_kwargs[-1] == 9

    result = single_pass(data, value=twice)

    assert result[0] == 0
    assert result[1] == 2
    assert result[-1] == 18
    assert result.sum() == 90
    assert result.sum() == sum(twice(data))


def test_basic_sanity_local_nested_func():
    """
    If this test fails but the one above
    succeeds, then the insertion of func
    objects into the function copy's
    `globals` is broken.
    """
    data = np.arange(10) * 2

    assert data[0] == 0
    assert data[1] == 2
    assert data[-1] == 18

    def square(x):
        return x * x

    assert square(2) == 4

    result = single_pass(data, value=square)

    assert result[0] == 0
    assert result[1] == 4
    assert result[-1] == 324
    assert square(2) == 4
    assert square(3) == 9


def test_math_function_supported():
    data = np.arange(0.1, 1.0, 0.1, dtype='float32')

    # TODO : get this working without the wrapper
    # function. Currently doesn't work due to
    # function not being found.
    def tanh(x):
        return math.tanh(x)

    assert tanh(0.5) == approx(math.tanh(0.5))

    result = single_pass(data, value=tanh)

    assert result[0] == approx(0.099668)
    assert result[1] == approx(0.19737533)
    assert result[2] == approx(0.29131263)
    assert sum(result) == approx(3.9521739)


def test_nested_math_function_supported():
    data = np.arange(10, dtype='float32')

    assert data[0] == approx(0.0)
    assert data[1] == approx(1.0)

    def calc(x):
        return 2 * math.log(x)

    assert calc(0.5) == approx(-1.38629436)

    # Assert ValueError for calling `log()`
    # on zero.
    # with raises(ValueError):
    #     _ = single_pass(data, value=calc)

    result = single_pass(data[1:], value=calc)

    assert result[0] == approx(0.0)
    assert result[1] == approx(1.38629436)
    assert result[2] == approx(2.19722462)
    assert result.sum() == approx(25.603655)


if __name__ == '__main__':
    import pytest
    pytest.main()