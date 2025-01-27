from pytest import fixture
from starlette.config import environ
from starlette.testclient import TestClient
from jose import jwt
import datetime
from main import app
from config import settings


@fixture(scope="module")
def test_client():
    client = TestClient(app)
    with client:
        yield client


@fixture(scope="session")
def test_client():
    with TestClient(app) as test_client:
        yield test_client


environ['TESTING'] = 'TRUE'


def get_headers():
    now = datetime.datetime.utcnow()
    JWT_SALT = settings.JWT_SALT
    token_payload = {
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "jti": "test_id",
        "exp": int((now + datetime.timedelta(days=1)).timestamp()),
        "identity": 'testuserID',
        "fresh": False,
        "type": "access",
        "user_claims": {
            "roles": [
                {
                    "name": "administrator",
                    "id": "testuserID"
                }
            ],
            "email": 'test@gmail.com'
        }
    }
    token = jwt.encode(token_payload, JWT_SALT, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}
