import hashlib


# def encode_md5(value: str) -> str:
#     hash_ = hashlib.md5(value.encode()).hexdigest()
#     print(hash_)
#     return hash_
#
#
# user_input = '44'
# user_input_encode = encode_md5(user_input)
# saved_password = 'f7177163c833dff4b38fc8d2872f1ec6'
# print(saved_password == user_input_encode)


from passlib.context import CryptContext

context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(value: str) -> str:
    hash_ = context.hash(value)
    print(hash_)
    return hash_


def verify_password(plain_password: str, hashed_password: str) -> bool:
    result = context.verify(plain_password, hashed_password)
    print(result)
    return result

# f7177163c833dff4b38fc8d2872f1ec6 md5
hashed_password_in_db = get_password_hash('44')

user_password = '45'

verify_password(user_password, hashed_password_in_db)
