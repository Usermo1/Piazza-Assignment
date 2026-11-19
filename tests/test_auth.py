from security import hash_password, verify_password

USER = {
    "username": "student",
    "email": "student@example.com",
    "password": "string123"}

def test_password_hash():
    hashed = hash_password(USER["password"])
    assert hashed != USER["password"]
    assert verify_password(USER["password"], hashed)
    assert not verify_password("wrongpassword", hashed)

def test_register_user(client):
    response = client.post("/auth/register", json=USER)

    assert response.status_code == 201
    assert response.json()["username"] == USER["username"]
    assert response.json()["email"] == USER["email"]

    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

def test_duplicate_registration(client):
    first = client.post(
        "/auth/register",
        json=USER
    )
    assert first.status_code == 201
    duplicate = client.post(
        "/auth/register",
        json=USER
    )
    assert duplicate.status_code == 409
    assert duplicate.json() == {
        "detail": "Email already registered"
    }


def test_login(client):
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
    response = login.json()
    assert "access_token" in response
    assert response["token_type"] == "bearer"


def test_wrong_password(client):
    client.post(
        "/auth/register",
        json=USER
    )
    login = client.post(
        "/auth/login",
        json={
            "email": USER["email"],
            "password": "wrongpassword"
        }
    )
    assert login.status_code == 401
    assert login.json() == {
        "detail": "Invalid email or password"
    }


def test_unknown_email(client):
    login = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "secret123"
        }
    )
    assert login.status_code == 401
    assert login.json() == {
        "detail": "Invalid email or password"
    }


def test_invalid_registration(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "st",
            "email": "not-an-email",
            "password": "123"
        }
    )
    assert response.status_code == 422