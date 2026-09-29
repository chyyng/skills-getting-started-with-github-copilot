from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_duplicate_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate-check@example.com"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"

    client.delete(f"/activities/{activity_name}/participants/{email}")


def test_unregister_participant_removes_their_email():
    # Arrange
    activity_name = "Chess Club"
    email = "remove-me@example.com"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities_response.json()[activity_name]["participants"]
