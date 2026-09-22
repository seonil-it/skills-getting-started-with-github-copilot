from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_avoids_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    second = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first.status_code == 200
    assert second.status_code == 400


def test_unregister_participant_removes_email():
    activity_name = "Soccer Club"
    email = "remove.me@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Unregistered {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]
