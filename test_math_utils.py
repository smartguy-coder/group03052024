from utils import math_utils


def test_sum_two():
    actual_result = math_utils.sum_two_numbers(2.0, 5.0)
    expected_result = 7.0
    assert actual_result == expected_result


def test_sum_two_2():
    actual_result = math_utils.sum_two_numbers(2, 5)
    expected_result = 7
    assert actual_result == expected_result
    assert isinstance(actual_result, float)
