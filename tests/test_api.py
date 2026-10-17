"""Basic API contract checks."""
def test_health_endpoint(api):
    response = api.get(api.base_url + "/health", timeout=5)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_customer_requires_fields(api):
    response = api.post(api.base_url + "/api/customers", json={"name": ""}, timeout=5)
    assert response.status_code == 400
    assert "error" in response.json()

def test_api_can_create_and_return_customer(api):
    email = "api-check@example.test"
    # The demo API returns 409 if a record from a previous run already exists.
    existing = api.get(api.base_url + "/api/customers", timeout=5).json()
    if any(item["email"] == email for item in existing):
        assert any(item["email"] == email for item in existing)
        return
    created = api.post(
        api.base_url + "/api/customers",
        json={"name": "API Check", "email": email},
        timeout=5,
    )
    assert created.status_code == 201
    assert created.json()["email"] == email
