from tests.conftest import get_headers
import datetime

activity_data = {
    "user_id": "testuserID",
    "creation_date": datetime.datetime.now().isoformat(),
    "operation": "create",
    "model": "project",
    "status": "success"
}

invalid_activity_data = {
    "creation_date": datetime.datetime.now().isoformat(),
    "operation": "create",
    "model": "project",
    "status": "success"
}

incorrect_activity_data_type = {
    "creation_date": datetime.datetime.now().isoformat(),
    "operation": 1,
    "model": 78,
    "status": "success"
}


def test_index(test_client):
    response = test_client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Logger API"}


def test_add_activity(test_client):
    # Test adding a new activity
    response = test_client.post("/api/activities", json=activity_data)
    assert response.status_code == 200
    assert response.json() == {"message": "activity added successfully"}


def test_add_activity_missing_fields(test_client):
    # Test adding activity with missing required fields
    invalid_activity_data = {key: value for key,
                             value in activity_data.items() if key != "user_id"}
    response = test_client.post("/api/activities", json=invalid_activity_data)
    assert response.status_code == 422


def test_get_activities(test_client):
    response = test_client.post("/api/activities", json=activity_data)
    # Test retrieving activities
    response = test_client.get("/api/activities", headers=get_headers())
    assert response.status_code == 200
    # assert response.json() != []


def test_get_activities_invalid_auth(test_client):
    # Test retrieving activities with invalid or missing authentication
    invalid_headers = {"Authorization": "Bearer InvalidToken"}
    response = test_client.get("/api/activities", headers=invalid_headers)
    assert response.status_code == 403


def test_get_activities_filtering(test_client):
    pass
