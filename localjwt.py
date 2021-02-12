import jwt
import datetime
import pytz


def is_jwt_valid(token):
    try:
        token_info = jwt.decode(token, options={"verify_signature": False})
    except:
        return False
    now = datetime.datetime.now()
    exp = datetime.datetime.fromtimestamp(token_info['exp'])
    print(f'now: {now}')
    print(f'exp: {exp}')
    return now < exp

