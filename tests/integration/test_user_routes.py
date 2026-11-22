
def test_register_user(client):
    """Verify that the API can register a new user."""

    response = client.post(
        "/users/register",
        json={
            "username": "integration_test",
            "email": "integration_test@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "integration_test"
    assert data["email"] == "integration_test@example.com"
    assert "id" in data

    # Password information should never be returned.
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_username(client):
    """Verify that duplicate usernames are rejected."""

    client.post(
        "/users/register",
        json={
            "username": "duplicate_user",
            "email": "first@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/users/register",
        json={
            "username": "duplicate_user",
            "email": "second@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 409
    assert response.json()["error"] == "Username or email already exists."


def test_register_duplicate_email(client):
    """Verify that duplicate email addresses are rejected."""

    client.post(
        "/users/register",
        json={
            "username": "first_user",
            "email": "duplicate@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/users/register",
        json={
            "username": "second_user",
            "email": "duplicate@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 409
    assert response.json()["error"] == "Username or email already exists."


def test_login_user(client):
    """Verify that a registered user can log in."""

    client.post(
        "/users/register",
        json={
            "username": "login_test",
            "email": "login_test@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "username": "login_test",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "login_test"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_login_incorrect_password(client):
    """Verify that an incorrect password is rejected."""

    client.post(
        "/users/register",
        json={
            "username": "wrong_password_test",
            "email": "wrong_password@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/users/login",
        json={
            "username": "wrong_password_test",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401
    assert response.json()["error"] == "Invalid username or password."


def test_login_nonexistent_user(client):
    """Verify that login fails for a nonexistent username."""

    response = client.post(
        "/users/login",
        json={
            "username": "unknown_user",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 401
    assert response.json()["error"] == "Invalid username or password."


def test_browse_users(client):
    """Verify that the API can retrieve registered users."""

    client.post(
        "/users/register",
        json={
            "username": "browse_test",
            "email": "browse_test@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.get("/users/")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1
    assert users[0]["username"] == "browse_test"


def test_read_user(client):
    """Verify that the API can retrieve a user by ID."""

    create_response = client.post(
        "/users/register",
        json={
            "username": "read_test",
            "email": "read_test@example.com",
            "password": "SecurePass123!"
        }
    )

    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["username"] == "read_test"


def test_read_user_not_found(client):
    """Verify that the API returns 404 for a nonexistent user."""

    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["error"] == "User not found."
