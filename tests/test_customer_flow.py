"""Integrated API -> browser UI -> database test."""
import uuid
from pages.customers_page import CustomersPage
from utils.db import find_customer_by_email

BASE_URL = "http://127.0.0.1:5000"

def test_customer_created_by_api_is_visible_in_ui_and_database(api, browser_page):
    unique = uuid.uuid4().hex[:10]
    name = f"Test Customer {unique}"
    email = f"{unique}@example.test"

    # 1. Arrange: create data using the API (faster than filling a UI form).
    response = api.post(
        api.base_url + "/api/customers",
        json={"name": name, "email": email},
        timeout=5,
    )
    assert response.status_code == 201
    customer = response.json()
    assert customer["name"] == name
    assert customer["email"] == email

    # 2. Act/verify: open the UI and check that the new customer is displayed.
    customers_page = CustomersPage(browser_page).open(BASE_URL)
    assert customers_page.heading.is_visible()
    assert customers_page.has_customer(email)

    # 3. Verify persistence: check that the record exists in SQLite.
    db_row = find_customer_by_email(email)
    assert db_row is not None
    assert db_row[1] == name
    assert db_row[2] == email
