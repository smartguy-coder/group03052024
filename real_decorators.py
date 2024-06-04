from functools import wraps
from typing import Callable

force_value_to_float = True

db = {"login": "admin", "password": "123"}


# def do_base_template_decorator(func: Callable):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         return result
#     return wrapper


def auth_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # data1, data2, *other = args
        # print(*args)
        # print(kwargs)
        print(1111111111)
        login = input("Enter login: ")
        password = input("Enter password: ")
        if login == db["login"] and password == db["password"]:
            result = func(*args, **kwargs)
            print(2222222)
            return result
        print(2222222)
        return None

    return wrapper


def force_to_dict_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return {"result": result, "status": "OK"}

    return wrapper


def force_value_to_float_decorator(use=True):
    def force_value_to_float_decorator_inner(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(5555555)
            result = func(*args, **kwargs)
            if isinstance(result, int) and use:
                result = float(result)
            print(66666666)
            return result

        return wrapper

    return force_value_to_float_decorator_inner


def write_logs_file_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        with open("log.csv", mode="a") as log_file:
            log_file.write(f"{func.__name__};{args};{kwargs};{result}\n")

        return result

    return wrapper


# add_two_numbers = auth_decorator( add_two_numbers )
# @auth_decorator
@force_to_dict_decorator
@force_value_to_float_decorator(force_value_to_float)
@write_logs_file_decorator
def add_two_numbers(number_1: float | int, number_2: float | int) -> float | int:
    result = number_1 + number_2
    print(80000000000)
    return result


@auth_decorator
@force_to_dict_decorator
def mult_two_numbers(number_1: float | int, number_2: float | int) -> float | int:
    result = number_1 * number_2
    return result


print(add_two_numbers(3, number_2=9))
print(add_two_numbers.__name__)
# print(mult_two_numbers(3, 9))
