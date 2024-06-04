# def like_lambda(first_number, second_number, *args):
#     result = first_number * second_number
#     return result
#
# cacl = {
#     'mult': lambda first_number, second_number, *args: first_number * second_number,
#     'pr': print,
#     'number': 444,
#     'like': like_lambda
# }
#
#
# def foo():
#     print(6666)
import datetime
from typing import Callable

db = {"login": "admin", "password": "123"}
# foo()
# foo.new_value = 888
# print(type(foo))
# print(foo.new_value)

# first = 2
# second = 5
# # result = cacl['number']
# result = cacl['mult'](first, second, 9999)
# result = cacl['like'].__name__
# print(result)
# def log(message: str) -> str:
#     result = f'{datetime.datetime.utcnow()} == {message}'
#     n(result)
#     return result
#
#
# def wrapper(func: Callable, arg: str) -> None:
#     new_arg = arg * 2
#     wrapper_result = func(new_arg)
#     return wrapper_result
#
#
# resut = wrapper(func=log, arg='5555')
# print(resut)


# #####################################################
def log(message: str) -> str:
    result = f"{datetime.datetime.utcnow()} == {message}"
    return result


def log2(message: str) -> str:
    result = f"{datetime.datetime.utcnow()} >>>> {message}"
    return result


def add_two_numbers(number_1: float | int, number_2: float | int) -> float | int:
    result = number_1 + number_2
    return result


def simple_decorator(func: Callable):
    def wrapper(*args, **kwargs):
        # data1, data2, *other = args
        # print(*args)
        # print(kwargs)
        login = input("Enter login: ")
        password = input("Enter password: ")
        if login == db["login"] and password == db["password"]:
            result = func(*args, **kwargs)
            return result
        return None

    return wrapper


log = simple_decorator(func=log)
log2 = simple_decorator(func=log2)
add_two_numbers = simple_decorator(func=add_two_numbers)


# print(log("ggggg"))
# print(log2("ggggg"))
print(add_two_numbers(number_1=2, number_2=8))
# print(log)

# bad example
# class Function:
#     def __str__(self):
#         return f'<function log at 0x104f35120 000>'
#
#     def __init__(self):
#         print('from init')
#
#     def __call__(self):
#         return lambda: lambda: lambda: lambda: lambda: 66777
# res = Function()()()()()()()
# print(res)
