from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_duplicate_rejected():
    activity_name = "Chess Club"
    email = "duplicate-check@example.com"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    client.delete(f"/activities/{activity_name}/participants/{email}")


def test_unregister_participant():
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
