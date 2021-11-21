from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome"}


def test_status():
    response = client.get("/status/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}


def test_timezone():
    response = client.get("/timezone?latitude=59.93&longitude=30.332")
    assert response.status_code == 200
    assert response.json() == {
        "latitude": 59.93,
        "longitude": 30.332,
        "timezone": "Europe/Moscow"
    }


def test_timezonel():
    response = client.get("/timezonel?latitude=59.93&longitude=30.332")
    assert response.status_code == 200
    assert response.json() == {
        "latitude": 59.93,
        "longitude": 30.332,
        "timezone": "Europe/Moscow"
    }


def test_timezone_post():
    response = client.post(
        "/timezone",
        json=[
            {
                "latitude": 59.93,
                "longitude": 30.332,
                "id": 0
            },
            {
                "latitude": 38.85,
                "longitude": -105.84,
                "id": 1
            }
        ])
    assert response.status_code == 200
    assert response.json() == [
        {
            "latitude": 59.93,
            "longitude": 30.332,
            "id": 0,
            "timezone": "Europe/Moscow"
        },
        {
            "latitude": 38.85,
            "longitude": -105.84,
            "id": 1,
            "timezone": "America/Denver"
        }
    ]


def test_timezonel_post():
    response = client.post(
        "/timezonel",
        json=[
            {
                "latitude": 59.93,
                "longitude": 30.332,
                "id": 0
            },
            {
                "latitude": 38.85,
                "longitude": -105.84,
                "id": 1
            }
        ])
    assert response.status_code == 200
    assert response.json() == [
        {
            "latitude": 59.93,
            "longitude": 30.332,
            "id": 0,
            "timezone": "Europe/Moscow"
        },
        {
            "latitude": 38.85,
            "longitude": -105.84,
            "id": 1,
            "timezone": "America/Denver"
        }
    ]
