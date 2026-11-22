
def test_browse_calculations(client):
    """Verify that the API can retrieve all calculations."""

    response = client.get("/calculations/")

    assert response.status_code == 200
    assert response.json() == []


def test_browse_calculations_with_records(client):
    """Verify that the API can retrieve a list of calculations."""

    client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Add"}
    )

    response = client.get("/calculations/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["result"] == 15


def test_create_calculation(client):
    """Verify that the API can create a calculation."""

    response = client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Add"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15


def test_read_calculation(client):
    """Verify that the API can retrieve a calculation by ID."""

    create_response = client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Add"}
    )

    calculation_id = create_response.json()["id"]

    response = client.get(f"/calculations/{calculation_id}")

    assert response.status_code == 200
    assert response.json()["id"] == calculation_id
    assert response.json()["result"] == 15


def test_update_calculation(client):
    """Verify that the API can update an existing calculation."""

    create_response = client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Add"}
    )

    calculation_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calculation_id}",
        json={"a": 20, "b": 4, "type": "Multiply"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == calculation_id
    assert data["a"] == 20
    assert data["b"] == 4
    assert data["type"] == "Multiply"
    assert data["result"] == 80


def test_delete_calculation(client):
    """Verify that the API can delete an existing calculation."""

    create_response = client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Add"}
    )

    calculation_id = create_response.json()["id"]

    response = client.delete(f"/calculations/{calculation_id}")

    assert response.status_code == 200

    # Confirm the calculation no longer exists.
    read_response = client.get(f"/calculations/{calculation_id}")

    assert read_response.status_code == 404


def test_read_calculation_not_found(client):
    """Verify that the API returns 404 for a nonexistent calculation."""

    response = client.get("/calculations/999999")

    assert response.status_code == 404
    assert response.json()["error"] == "Calculation not found."


def test_update_calculation_not_found(client):
    """Verify that updating a nonexistent calculation returns 404."""

    response = client.put(
        "/calculations/999999",
        json={"a": 20, "b": 4, "type": "Multiply"}
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Calculation not found."


def test_delete_calculation_not_found(client):
    """Verify that deleting a nonexistent calculation returns 404."""

    response = client.delete("/calculations/999999")

    assert response.status_code == 404
    assert response.json()["error"] == "Calculation not found."


def test_divide_by_zero(client):
    """Verify that the API rejects division by zero."""

    response = client.post(
        "/calculations/",
        json={"a": 10, "b": 0, "type": "Divide"}
    )

    assert response.status_code == 400


def test_invalid_calculation_type(client):
    """Verify that the API rejects unsupported calculation types."""

    response = client.post(
        "/calculations/",
        json={"a": 10, "b": 5, "type": "Power"}
    )

    assert response.status_code == 400



def test_non_finite_calculation_value(client):
    """Verify that the API rejects non-finite numbers."""

    response = client.post(
        "/calculations/",
        content='{"a": NaN, "b": 5, "type": "Add"}',
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400

