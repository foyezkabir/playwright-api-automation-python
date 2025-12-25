# Playwright API Automation (Python)

This project contains an API automation suite for testing user signup functionality using **Playwright** and **Python (pytest)**.

## Project Structure

- `test_signup.py`: Contains all API test cases (Success, Validation, Error Handling).
- `requirements.txt`: List of project dependencies.

## Setup

1.  **Clone the repository** (or download the source).
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment**:
    - Windows: `.\venv\Scripts\activate`
    - Mac/Linux: `source venv/bin/activate`
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

## Running Tests

Run the tests using `pytest`:

```bash
pytest test_signup.py
```

## Test Coverage

The suite covers:
- ✅ **Happy Path**: Successful user registration.
- ✅ **Field Validation**: Missing fields, invalid email format.
- ✅ **Public Domain Check**: Blocking emails from public domains (gmail, yahoo, etc.).
- ⚠️ **Known Issues (Marked as xfail)**:
    - Name validation (min/max length, special chars, numbers).
    - Password complexity (API returns 500 error).
    - Password mismatch (API ignores mismatch).
