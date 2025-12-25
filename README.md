# Playwright API Automation (Python)

This project demonstrates a robust API automation suite for testing user signup functionality using **Playwright** and **Python (pytest)**.

## 📖 Project Overview

The goal of this project was to create an automated test suite for the Signup API endpoint, validating it against the requirements derived from the UI design (Figma). We focused on verifying that the **Backend API** enforces the same strict validation rules presented on the **Frontend UI**.

## 🎨 From Figma to API Tests

We started by analyzing the **Figma/UI Design** of the Signup page to understand the expected behavior and validation rules.

**What we derived from the UI:**
1.  **Fields Identified**: `Name`, `Email`, `Password`, `Confirm Password`.
2.  **Validation Rules**:
    -   **Name**: Must not contain numbers, special characters, or be too short/long.
    -   **Email**: Must be a valid format and **cannot** be a public domain (e.g., gmail, yahoo).
    -   **Password**: Must meet complexity requirements (Uppercase, Lowercase, Number, Special Character).
    -   **Consistency**: Password and Confirm Password must match.

**The Testing Strategy:**
We wrote API tests to bypass the Frontend and send requests directly to the Backend. This ensures that the API is secure and self-validating, not relying solely on the UI for data integrity.

## 🔗 API Details

-   **Base URL**: `https://eks-dev-lb.shadhinlab.xyz`
-   **Endpoint**: `/api/authentication/signup/`
-   **Method**: `POST`
-   **Payload**:
    ```json
    {
      "name": "Test User",
      "email": "user@company.com",
      "password": "Password123!",
      "confirm_password": "Password123!"
    }
    ```

## 🧪 Test Scenarios & Findings

We implemented tests to cover both "Happy Paths" and "Edge Cases".

### ✅ Passing Tests (Working as Expected)
-   **Successful Signup**: Valid data creates a user (200/201 OK).
-   **Missing Fields**: API correctly rejects requests with missing required fields (400 Bad Request).
-   **Public Domain Emails**: API correctly blocks emails from `gmail.com`, `yahoo.com`, etc.

### ⚠️ Critical Findings (Bugs / Missing Validations)
We discovered significant discrepancies between the UI rules and the API behavior. These tests are marked as `xfail` (Expected Failure) in the suite:

1.  **Name Validation Missing**:
    -   The API **accepts** names with numbers (e.g., `User123`), whereas the UI says "Name not allow any number".
    -   The API **accepts** names with special characters (e.g., `@User`) and leading/trailing spaces.
2.  **Password Complexity Error**:
    -   When a password lacks complexity (e.g., no uppercase), the API returns a **500 Internal Server Error** instead of a 400 Validation Error. This is a critical stability issue.
3.  **Password Mismatch**:
    -   The API **accepts** the request even if `password` and `confirm_password` do not match.

## ⚙️ Setup & Usage

### Prerequisites
-   Python 3.8+
-   pip

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/foyezkabir/playwright-api-automation-python.git
    cd playwright-api-automation-python
    ```
2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

### Running Tests
Run the full test suite using pytest:
```bash
pytest test_signup.py
```
