from fastapi.testclient import TestClient
from app.routes import router
from app.model import Activity
# from unittest.mock import patch
from jose import jwt
import os
import datetime

# from app.tasks import create_celery

client = TestClient(router)


def generate_token():
    now = datetime.datetime.utcnow()
    JWT_SECRET = os.getenv("JWT_SALT", "SALT")
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
                    "id": "test_id"
                }
            ],
            "email": 'test@gmail.com'
        }
    }
    return jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world"}


def test_add_activity():
    data = {"user_id": "testuserID", "creation_date": datetime.datetime.now().isoformat(),
            "operation": "create", "model": "project", "status": "success"}
    response = client.post("/activities", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "activity added successfully"}


def test_get_activities():
    token = generate_token()
    headers = {"access-token": token}
    response = client.get("/activities", headers=headers)
    assert response.status_code == 200
