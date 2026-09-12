from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_person():
    response = client.post(
        "/api/v1/persons",
        json={
            "name": "Test Person",
            "age": 25,
            "address": "Moscow",
            "work": "Engineer"
        }
    )

    assert response.status_code == 201
    assert response.text == ""
    assert "location" in response.headers
    assert response.headers["location"].startswith("/api/v1/persons/")

def test_get_person():
    create_response = client.post(
        "/api/v1/persons",
        json={
            "name": "Get Test",
            "age": 30,
            "address": "Moscow",
            "work": "Developer"
        }
    )

    person_id = create_response.headers["location"].split("/")[-1]

    response = client.get(f"/api/v1/persons/{person_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == int(person_id)
    assert data["name"] == "Get Test"
    assert data["age"] == 30
    assert data["address"] == "Moscow"
    assert data["work"] == "Developer"

def test_get_person_not_found():
    response = client.get("/api/v1/persons/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"

def test_update_person():
    create_response = client.post(
        "/api/v1/persons",
        json={
            "name": "Original Name",
            "age": 25,
            "address": "Original Address",
            "work": "Engineer"
        }
    )

    person_id = create_response.headers["location"].split("/")[-1]

    response = client.patch(
        f"/api/v1/persons/{person_id}",
        json={
            "name": "Updated Name"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == int(person_id)
    assert data["name"] == "Updated Name"

    # Các field không được sửa phải giữ nguyên
    assert data["age"] == 25
    assert data["address"] == "Original Address"
    assert data["work"] == "Engineer"

def test_delete_person():
    create_response = client.post(
        "/api/v1/persons",
        json={
            "name": "Delete Test",
            "age": 40,
            "address": "Moscow",
            "work": "Tester"
        }
    )

    person_id = create_response.headers["location"].split("/")[-1]

    response = client.delete(
        f"/api/v1/persons/{person_id}"
    )

    assert response.status_code == 204
    assert response.text == ""

    get_response = client.get(
        f"/api/v1/persons/{person_id}"
    )

    assert get_response.status_code == 404