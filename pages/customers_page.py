"""Page Object Model for the customer portal."""
class CustomersPage:
    def __init__(self, page):
        self.page = page
        self.heading = page.get_by_role("heading", name="Customer Portal")
        self.table = page.locator("#customers-table")

    def open(self, base_url):
        self.page.goto(base_url)
        return self

    def has_customer(self, email):
        return self.page.locator(f'tr[data-email="{email}"]').count() > 0
