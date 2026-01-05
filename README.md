# Playwright API Automation with Enhanced Reporting & AI Analytics (Python)

This project demonstrates a **production-ready API automation framework** for testing user authentication APIs using **Playwright**, **Python (pytest)**, **Allure Reports**, and **ReportPortal** for AI-powered test analytics.

## 📖 Project Overview

The goal of this project was to create an automated test suite for the Signup API endpoint, validating it against the requirements derived from the UI design (Figma). We focused on verifying that the **Backend API** enforces the same strict validation rules presented on the **Frontend UI**.

### 🎯 Key Features

✨ **Enhanced Test Infrastructure**
- 🏭 **Test Data Factory** - Realistic test data generation with Faker
- 🌍 **Multi-Environment Support** - Dev/Staging/Prod configuration
- 🔄 **Auto-Retry Mechanism** - Automatic retry for flaky tests
- ⚡ **Parallel Execution** - Fast test runs with pytest-xdist
- ✅ **Schema Validation** - Pydantic models for API response validation

📊 **Advanced Reporting**
- 📈 **Allure Reports** - Rich interactive HTML reports with attachments
- 🤖 **ReportPortal Integration** - AI-powered test analytics & failure categorization
- 📧 **Slack Notifications** - Real-time alerts on test failures
- 📋 **Test Coverage Matrix** - Comprehensive documentation of test scenarios

🚀 **CI/CD Excellence**
- ✅ **GitHub Actions** - Automated testing on every commit
- 🔀 **Matrix Testing** - Test across multiple Python versions
- 📦 **Artifact Management** - Automatic upload of test results
- 🔔 **PR Comments** - Test results posted directly on pull requests
- 🌙 **Nightly Regression** - Scheduled full test suite execution

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
    playwright install chromium
    ```
4.  **Configure environment** (optional):
    ```bash
    # Copy example env file
    copy .env.example .env
    
    # Edit .env with your configuration
    # Set BASE_URL, RP_UUID, SLACK_WEBHOOK_URL, etc.
    ```

### Running Tests

#### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest test_signup.py

# Run with verbose output
pytest -v

# Run specific test
pytest test_signup.py::TestSignup::test_signup_success
```

#### Parallel Execution (Fast)
```bash
# Auto-detect CPU cores and run in parallel
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

#### With Retry for Flaky Tests
```bash
# Retry failed tests up to 2 times
pytest --reruns 2 --reruns-delay 1
```

#### Generate Allure Report
```bash
# Run tests and generate Allure results
pytest --alluredir=./allure-results

# Generate and open HTML report
allure serve ./allure-results
```

#### With ReportPortal Integration
```bash
# First, configure ReportPortal (see docs/REPORTPORTAL_SETUP.md)
# Then run with --reportportal flag
pytest --reportportal

# Or set in .env: REPORT_PORTAL_ENABLED=true
pytest
```

### Configuration Options

All configuration is managed through `.env` file or environment variables:

```bash
# Environment
ENV=dev                          # dev, staging, prod

# API Configuration
BASE_URL=https://eks-dev-lb.shadhinlab.xyz
API_TIMEOUT=30

# Test Execution
RETRY_COUNT=2
PARALLEL_WORKERS=4

# Reporting
ALLURE_RESULTS_DIR=./allure-results
REPORT_PORTAL_ENABLED=false
RP_ENDPOINT=http://localhost:8080
RP_PROJECT=api_automation
RP_UUID=your-uuid-here

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## 🚀 CI/CD Pipeline

This project uses **GitHub Actions** for Continuous Integration with advanced features:

### Features
- ✅ **Multi-Version Testing** - Tests run on Python 3.11 and 3.12
- ⚡ **Parallel Execution** - Fast test runs with pytest-xdist
- 🔄 **Auto-Retry** - Automatic retry of flaky tests
- 📊 **Allure Reports** - Rich HTML reports published to GitHub Pages
- 🤖 **ReportPortal** - AI-powered analytics (when enabled)
- 📧 **Slack Notifications** - Real-time alerts on failures
- 💬 **PR Comments** - Test results posted directly on pull requests
- 🌙 **Scheduled Runs** - Nightly full regression at 2 AM UTC
- 🔧 **Manual Triggers** - Run on-demand with environment selection

### Workflow File
Located at [`.github/workflows/api-tests.yml`](.github/workflows/api-tests.yml)

### Triggers
- **Push** to `main` or `develop` branches
- **Pull Requests** to `main` or `develop`
- **Scheduled** - Daily at 2 AM UTC
- **Manual** - Via workflow_dispatch with environment selection

### Pipeline Steps
1.  **Environment Setup**: Ubuntu runner with Python 3.11/3.12
2.  **Dependency Installation**: Installs all requirements and Playwright browsers
3.  **Configuration**: Creates `.env` file from GitHub Secrets
4.  **Test Execution**: Runs tests with parallel execution and retries
5.  **Allure Report Generation**: Creates rich HTML reports
6.  **Artifact Upload**: Saves test results and reports
7.  **GitHub Pages Deployment**: Publishes Allure report (main branch only)
8.  **Notifications**: Sends Slack notifications and PR comments

### Required GitHub Secrets
Configure these in your repository settings (Settings → Secrets and variables → Actions):

```
BASE_URL              # API base URL
RP_ENABLED            # true/false for ReportPortal
RP_ENDPOINT           # ReportPortal URL (optional)
RP_PROJECT            # ReportPortal project name (optional)
RP_UUID               # ReportPortal API token (optional)
SLACK_WEBHOOK_URL     # Slack webhook for notifications (optional)
```

### Viewing Results
1.  **GitHub Actions Tab** - View workflow runs and logs
2.  **Allure Report** - https://your-username.github.io/your-repo/allure-report
3.  **Artifacts** - Download from workflow run page
4.  **ReportPortal** - View AI-powered analytics at your RP instance
5.  **Slack** - Receive notifications in configured channel

## 📊 Test Coverage & Documentation

### Test Coverage Matrix
Comprehensive documentation of all test scenarios, results, and known issues:
- 📄 [TEST_COVERAGE.md](docs/TEST_COVERAGE.md) - Detailed test coverage matrix

### ReportPortal Setup
Complete guide for AI-powered test analytics integration:
- 📘 [REPORTPORTAL_SETUP.md](docs/REPORTPORTAL_SETUP.md) - Step-by-step setup guide

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── api-tests.yml         # CI/CD pipeline configuration
├── test_signup.py                # Main test suite
├── api_objects.py                # API client wrapper
├── conftest.py                   # Pytest fixtures
├── config.py                     # Environment configuration
├── data_factory.py               # Test data generation with Faker
├── schemas.py                    # Pydantic models for validation
├── reportportal_helpers.py       # ReportPortal utilities
├── pytest.ini                    # Pytest configuration
├── reportportal.ini              # ReportPortal configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
├── README.md                     # This file
└── docs/                         # Documentation folder
    ├── GETTING_STARTED.md        # Quick start guide
    ├── QUICK_REFERENCE.md        # Command reference
    ├── TEST_COVERAGE.md          # Test coverage documentation
    ├── REPORTPORTAL_SETUP.md     # ReportPortal setup guide
    ├── GITHUB_SECRETS_SETUP.md   # CI/CD secrets setup
    ├── IMPLEMENTATION_SUMMARY.md # Implementation details
    └── ARCHITECTURE.md           # Framework architecture
```

## 🛠️ Advanced Usage

### Using Test Data Factory

```python
from data_factory import UserDataFactory

# Generate realistic test data
payload = UserDataFactory.create_signup_payload(
    name="John Doe",
    email=UserDataFactory.random_email(domain="example.com")
)

# Create invalid payload for negative testing
invalid_payload = UserDataFactory.create_invalid_payload(
    field_to_invalidate="email",
    invalid_value="not-an-email"
)

# Security testing payloads
from data_factory import AttackVectorFactory
sql_payloads = AttackVectorFactory.sql_injection_payloads()
xss_payloads = AttackVectorFactory.xss_payloads()
```

### Schema Validation

```python
from schemas import SignupSuccessResponseSchema, assert_response_schema

# Validate response against schema
response = signup_api.create_user(payload)
response_data = response.json()

assert_response_schema(
    response_data, 
    SignupSuccessResponseSchema,
    "Signup response validation failed"
)
```

### ReportPortal Logging

```python
from reportportal_helpers import ReportPortalHelper

# Log API request
ReportPortalHelper.log_request(
    test_name="test_signup",
    method="POST",
    url="/api/authentication/signup/",
    payload=payload
)

# Log API response
ReportPortalHelper.log_response(
    test_name="test_signup",
    status_code=200,
    response_body=response.json(),
    response_time_ms=250
)

# Report a bug
ReportPortalHelper.log_bug(
    bug_id="BUG-123",
    description="Password validation returns 500",
    severity="CRITICAL"
)
```

## 🐛 Known Issues & Findings

### Critical Issues (P0)
1. **Password Complexity Validation Returns 500 Error**
   - API returns Internal Server Error instead of validation error
   - Affects user experience and indicates server instability

### High Priority Issues (P1)
2. **No Name Validation**
   - API accepts names with numbers, special characters
   - Inconsistent with UI validation rules

3. **Password Mismatch Not Validated**
   - API doesn't verify password and confirm_password match
   - User can create account with unintended password

See [TEST_COVERAGE.md](docs/TEST_COVERAGE.md) for complete issue list.

## 📈 Roadmap

### ✅ Completed
- [x] Basic signup API tests
- [x] Test data factory with Faker
- [x] Multi-environment configuration
- [x] Auto-retry mechanism
- [x] Parallel test execution
- [x] Allure reporting
- [x] ReportPortal integration
- [x] GitHub Actions CI/CD
- [x] Slack notifications
- [x] Test coverage documentation

### 🚧 In Progress
- [ ] Login API tests
- [ ] Duplicate email validation test
- [ ] Security testing (SQL injection, XSS)

### 📅 Planned
- [ ] Profile Management API tests
- [ ] Password Reset API tests
- [ ] Database verification tests
- [ ] Performance/load testing
- [ ] Contract testing with OpenAPI
- [ ] End-to-end user journey tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Foyez Kabir**
- GitHub: [@foyezkabir](https://github.com/foyezkabir)

## 🙏 Acknowledgments

- Playwright Team for excellent API testing capabilities
- ReportPortal for AI-powered test analytics
- Open Source Community

---

**⭐ Star this repository if you find it helpful!**
