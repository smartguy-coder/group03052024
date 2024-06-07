from time import sleep

import jwt
import datetime as dt


JWT_KEY = 'kjfghfghjfjgfhjgfghfghfhfg8767868'

payload = {
    'my_name': 'Vasyl',
    'age': 45,
    'exp': dt.datetime.utcnow() + dt.timedelta(seconds=4),
    'iat': dt.datetime.utcnow(),
}


def encode_jwt(payload_data: dict) -> str:
    encode_jwt_ = jwt.encode(
        payload=payload_data,
        key=JWT_KEY,
        algorithm='HS256'
    )
    return encode_jwt_


def decode_jwt(encoded_jwt: str) -> dict:
    try:
        decoded_data = jwt.decode(
            jwt=encoded_jwt,
            key=JWT_KEY,
            algorithms=['HS256'],
            # options={
            #     'verify_signature': False
            # }
        )
        return decoded_data
    except jwt.exceptions.ExpiredSignatureError:
        print('jwt.exceptions.ExpiredSignatureError')
    except jwt.exceptions.InvalidSignatureError:
        print('jwt.exceptions.InvalidSignatureError')


print(decode_jwt(encode_jwt))

