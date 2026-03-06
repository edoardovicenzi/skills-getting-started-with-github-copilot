from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_signup_and_remove_participant():
    # choose an activity that exists
    activity = "Chess Club"
    email = "tester@mergington.edu"

    # ensure not already enrolled
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    data = resp.json()
    assert "Signed up" in data.get("message", "")
    assert email in activities[activity]["participants"]

    # remove
    resp2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert "Removed" in data2.get("message", "")
    assert email not in activities[activity]["participants"]


def test_remove_nonexistent_participant():
    activity = "Chess Club"
    email = "idontexist@mergington.edu"

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    # should return 400 because not registered
    assert resp.status_code == 400


def test_remove_from_unknown_activity():
    resp = client.delete("/activities/NoActivity/participants?email=test@x.com")
    assert resp.status_code == 404
