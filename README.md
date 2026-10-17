# Hybrid End-to-End Test Framework (Beginner-Friendly)

A small, runnable portfolio project demonstrating **API + browser UI + SQL database** testing in one flow.

## What this project does

1. Starts a local demo web app.
2. Creates a customer through its REST API.
3. Opens the web page with Playwright and checks that the customer appears.
4. Queries SQLite directly to confirm the record was saved.
5. Saves test-run results and builds a simple HTML dashboard with pass rate, duration, and failed/flaky-test indicators.

> This is a learning/demo framework. It does not prove production experience. Run it yourself before listing measured metrics on a resume.

## Tech stack

- Python 3.10+
- Flask (tiny demo application)
- Playwright (browser automation)
- Pytest (test runner)
- Requests (API calls)
- SQLite (local database)
- HTML report dashboard
- GitHub Actions workflow (optional CI)

## 1. Install

Open a terminal inside this project folder.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies and the browser:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## 2. Run the demo app

In terminal window 1:

```bash
python app.py
```

Leave it running. The app is available at `http://127.0.0.1:5000`.

## 3. Run tests

Open terminal window 2 in the same folder:

```bash
pytest -v
```

The tests use the running demo app. They create records through the API, inspect the UI, and query SQLite.

## 4. Generate the dashboard

After running tests:

```bash
python reports/build_dashboard.py
```

Open `reports/dashboard.html` in your browser. The dashboard summarizes the recorded test runs. A first run may show only one run; flaky-test detection becomes meaningful after repeated runs.

## 5. Run tests and record a result in one command

With the demo app still running:

```bash
python run_and_report.py
```

This runs Pytest, stores a JSON run record, and refreshes the dashboard. It returns the test process exit code.

## Project map

```text
app.py                         Demo application, API routes, UI and SQLite setup
tests/test_customer_flow.py    Integrated API -> UI -> database test
tests/test_api.py              API validation examples
pages/customers_page.py        Small Page Object Model example
utils/db.py                    Database helper functions
utils/results.py               Test-run result storage
reports/build_dashboard.py     Creates the HTML dashboard
run_and_report.py               One-command test/report runner
.github/workflows/tests.yml    Example CI workflow
```

## Beginner glossary

- **End-to-end (E2E) test:** Checks a complete user workflow across multiple parts of an application.
- **REST API:** An interface that lets software send requests to an application, often using HTTP.
- **Pytest:** A Python tool that discovers and runs tests.
- **Playwright:** A browser automation tool used to click, type, and inspect web pages.
- **SQL / SQLite:** SQL is a language for querying data; SQLite stores the demo database in a local file.
- **Persistence:** Data remains stored after a request finishes.
- **Page Object Model (POM):** A pattern that keeps page locators and page actions in a separate class.
- **Pass rate:** Passed tests divided by all tests in a run, multiplied by 100.
- **Flaky test:** A test that sometimes passes and sometimes fails without a relevant code change. This project estimates flakiness from inconsistent outcomes across recorded runs; it needs repeated runs to be useful.
- **CI/CD:** Automated checks that can run when code is pushed or a pull request is opened.
- **Test setup time:** Time spent preparing state before the actual test action. This project uses API setup to avoid manually creating the test customer through the UI, but does not calculate a validated percentage reduction.

## Honest resume wording

Use this only after you have installed, run, and understood the project. Do not claim a percentage unless you measure it.

**Hybrid End-to-End Test Framework | Python, Playwright, Pytest, REST API, SQLite**
- Built an integrated test flow that creates customer data through a REST API, verifies it in the browser UI, and checks persistence in SQLite.
- Added reusable Pytest fixtures, a Page Object Model, and API validation tests for maintainable automation.
- Generated an HTML test-health dashboard showing run duration, pass rate, and tests with inconsistent outcomes across recorded runs.

If you want to include “reduced setup time by X%”, measure a baseline first; the repository intentionally does not invent that number.

## Troubleshooting

- **Connection refused:** Ensure `python app.py` is running in terminal 1.
- **Playwright browser missing:** Run `python -m playwright install chromium`.
- **Port 5000 already in use:** Stop the other app or change `BASE_URL` and the port consistently.
- **Database seems old:** Stop the app, delete `test_app.db`, then restart it. This resets local demo data.
- **Dashboard has no data:** Run `python run_and_report.py` after starting the app.

## Important

This is a local demo app and should not be used with real customer information. The example credentials/data are fictional.
