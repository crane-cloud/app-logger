from jose import JWTError, jwt
import os


def has_role(role_list: list, role_name: str) -> bool:
    for role in role_list:
        if role['name'] == role_name:
            return True
    return False


def get_current_user_claims(access_token: str) -> object:
    payload = jwt.decode(access_token, os.getenv(
        "JWT_SALT"), algorithms=['HS256'])
    return payload['user_claims']


def get_current_user_id(access_token: str) -> object:
    payload = jwt.decode(access_token, os.getenv(
        "JWT_SALT"), algorithms=['HS256'])
    return payload['identity']
