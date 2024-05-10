from typing import Union


def add_two_numbers(first_number: Union[int, float], second_number: int | float) -> int | float:
    """
    sums given numbers
    2 + 2 => 4
    """

    result = first_number + second_number
    return result


def send_email(address: str, body: dict) -> None:

    print("sending.....")


def is_equal(first_number: int, second_number: int) -> bool:
    result = first_number == second_number
    return result


print("-------", add_two_numbers(1.5, 99999999) + 55555)
