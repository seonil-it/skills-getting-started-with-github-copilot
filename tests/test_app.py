from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_avoids_duplicate_registration():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Soccer Club"
    email = "remove.me@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    activity = client.get("/activities").json()[activity_name]

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activity["participants"]
