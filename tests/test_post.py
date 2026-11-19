
from datetime import datetime, timedelta, timezone
USER = {
    "username": "student",
    "email": "student@example.com",
    "password": "string123"
}
def future_expiry():
    return (
        datetime.now(timezone.utc) + timedelta(days=1)
    ).isoformat()

def get_token(client):
    registered = client.post(
        "/auth/register",
        json=USER
    )
    assert registered.status_code == 201
    login = client.post(
        "/auth/login",
        json={
            "email": USER["email"],
            "password": USER["password"]
        }
    )
    assert login.status_code == 200
    return login.json()["access_token"]

def test_create_post_requires_authentication(client):
    response = client.post(
        "/posts/",
        json={
            "title": "Test post",
            "body": "Testing Piazza",
            "expires_at": future_expiry(),
            "topic_ids": [4]
        }
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_create_post(client):
    token = get_token(client)
    response = client.post(
        "/posts/",
        json={
            "title": "Technology post",
            "body": "Testing Piazza post creation",
            "expires_at": future_expiry(),
            "topic_ids": [4]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Technology post"
    assert data["body"] == "Testing Piazza post creation"
    assert data["author_id"] == 1

def test_post_requires_topic(client):
    token = get_token(client)
    response = client.post(
        "/posts/",
        json={
            "title": "No topic",
            "body": "This should fail",
            "expires_at": future_expiry(),
            "topic_ids": []
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 422

def test_invalid_topic(client):
    token = get_token(client)
    response = client.post(
        "/posts/",
        json={
            "title": "Invalid topic",
            "body": "This should fail",
            "expires_at": future_expiry(),
            "topic_ids": [999]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid topic ID"
    }

def test_duplicate_topics(client):
    token = get_token(client)
    response = client.post(
        "/posts/",
        json={
            "title": "Duplicate topics",
            "body": "This should fail",
            "expires_at": future_expiry(),
            "topic_ids": [4, 4]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Duplicate topic IDs are not allowed"
    }

def past_expiry():
    return (
        datetime.now(timezone.utc) - timedelta(days=1)
    ).isoformat()

def test_post_expiry_must_be_future(client):
    token = get_token(client)
    response = client.post(
        "/posts/",
        json={
            "title": "Expired post",
            "body": "This should fail",
            "expires_at": past_expiry(),
            "topic_ids": [4]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Expiry time must be in the future"
    }

def test_get_posts(client):
    token = get_token(client)
    created = client.post(
        "/posts/",
        json={
            "title": "Technology post",
            "body": "Testing retrieval",
            "expires_at": future_expiry(),
            "topic_ids": [4]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert created.status_code == 201
    response = client.get("/posts/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Technology post"

def test_get_post(client):
    token = get_token(client)
    created = client.post(
        "/posts/",
        json={
            "title": "Specific post",
            "body": "Testing retrieval by ID",
            "expires_at": future_expiry(),
            "topic_ids": [4]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert created.status_code == 201
    post_id = created.json()["id"]
    response = client.get(
        f"/posts/{post_id}"
    )
    assert response.status_code == 200
    assert response.json()["id"] == post_id
    assert response.json()["title"] == "Specific post"

def test_get_missing_post(client):
    response = client.get("/posts/9999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Post not found"
    }
