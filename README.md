# Playwright API Automation Framework with CI/CD (Python)

Production-ready API test automation framework for authentication APIs using **Playwright**, **Python (pytest)**, **Allure Reports**, and automated **CI/CD pipeline** with **GitHub Pages** deployment.

---

## ⚠️ Disclaimer

**This is an portfolio project created for demonstration purposes.**

While this framework tests a real API, the project showcases API test automation best practices, CI/CD implementation, and modern testing techniques. The code, methodologies, and architecture patterns demonstrated here are designed to exhibit professional testing capabilities.

- **Not Official Company Repository**: This is a personal learning project
- **Learning Purpose**: Demonstrates API testing and DevOps skills
- **Test Data**: All test data is auto-generated and non-sensitive
- **Public Access**: Suitable for portfolio and skill demonstration

---

## 📖 Project Overview

Comprehensive API testing framework for the complete user authentication flow including signup, email verification (OTP), and resend OTP functionality. Tests validate API behavior, security, and edge cases with extensive coverage. **Includes automated CI/CD pipeline** with GitHub Actions for continuous testing and report deployment.

### 🎯 Key Features

✨ **Modern Test Architecture**
- 🏭 **Test Data Factory** - Realistic data generation with Faker
- 🌍 **Multi-Environment Support** - Dev/Staging/Prod configuration
- 🔄 **Auto-Retry Mechanism** - Flaky test handling with pytest-rerunfailures
- ⚡ **Parallel Execution** - 12 workers with pytest-xdist
- ✅ **Response Validation** - Pydantic schemas for API contract validation
- 🎨 **Custom Decorators** - Organized test categorization (@api_smoke, @validation_test, @known_bug)

📊 **Advanced Reporting**
- 📈 **Allure Reports** - Rich interactive HTML reports with test history
- 🌐 **GitHub Pages** - Automated report deployment with every push
- 📋 **Test Coverage Matrix** - Comprehensive documentation (29 total tests)
- 🖼️ **Browser Validation** - Chrome DevTools MCP for UI verification

🚀 **CI/CD Pipeline** ([View Detailed Architecture](#-cicd-pipeline-architecture))
- ✅ **GitHub Actions** - Three-stage pipeline: Build → Test → Deploy
- 🔀 **Parallel Testing** - 12 concurrent workers for fast execution (~15-20 seconds)
- 📦 **Artifact Management** - Allure results preserved and deployed
- 🌐 **Auto Deployment** - Reports published to GitHub Pages automatically
- 🔗 **Live Report URL** - [View Reports](https://foyezkabir.github.io/playwright-api-automation-python/allure-report)
- ☁️ **Cloud Runners** - Tests run on GitHub-hosted Ubuntu runners in the cloud

---

## 🚀 CI/CD Pipeline Architecture

> **Note**: The CI/CD pipeline runs on **GitHub-hosted Ubuntu runners** (cloud infrastructure). Your local development is on **Windows**, and tests work on both platforms since Python and Playwright are cross-platform. When you push code from Windows, GitHub Actions automatically runs tests on Ubuntu in the cloud.

### Pipeline Flow
```
📤 Git Push (Windows) → ☁️ GitHub Actions (Ubuntu) → 🏗️ Build → 🧪 Test → 🚀 Deploy → 📊 Report Live
```

### Three-Stage Workflow

#### **Stage 1: Build** 🏗️
**Purpose**: Prepare the test environment and dependencies

**Steps**:
1. **Checkout Code**
   - Fetches latest code from repository
   - Uses `actions/checkout@v3`
   
2. **Setup Python Environment**
   - Installs Python 3.12 on Ubuntu runner
   - Configures pip cache for faster installs
   
3. **Install Dependencies**
   - Runs `pip install -r requirements.txt`
   - Installs all packages: pytest, playwright, allure-pytest, faker, pydantic, etc.
   
4. **Configure Environment**
   - Creates `.env` file with configuration:
     - `ENV=dev`
     - `BASE_URL=https://eks-dev-lb.shadhinlab.xyz`
     - `RETRY_COUNT=2`
     - `PARALLEL_WORKERS=12`
   - No secrets required (hardcoded dev environment)
   
5. **Cache Artifacts**
   - Uploads build directory as artifact
   - Enables dependency sharing between jobs
   - **Duration**: ~5-8 seconds

**Job Name**: `build`  
**Runs on**: `ubuntu-latest` (GitHub-hosted runner in cloud)  
**Your Local**: Windows 11 (development environment)

---

#### **Stage 2: Test** 🧪
**Purpose**: Execute all test cases and generate results

**Steps**:
1. **Download Build Artifacts**
   - Retrieves cached build from Stage 1
   - Restores Python environment and dependencies
   
2. **Execute Tests with Pytest**
   ```bash
   pytest -n 12 -v --reruns 3 --alluredir=./allure-results
   ```
   - `-n 12`: Runs 12 tests in parallel (pytest-xdist)
   - `-v`: Verbose output with test names
   - `--reruns 3`: Auto-retry failed tests up to 3 times
   - `--alluredir`: Generates Allure JSON results
   
3. **Test Execution**
   - **Signup Tests**: 19 tests (test_signup.py)
   - **Verification Tests**: 5 tests (test_signup_verification.py)
   - **Resend OTP Tests**: 5 tests (test_signup_verification.py)
   - **Total**: 29 tests executed
   
4. **Generate Test Results**
   - Creates `allure-results/` directory with:
     - Test case JSON files
     - Attachments (request/response logs)
     - Test execution metadata
     - History data for trends
   
5. **Upload Artifacts**
   - Packages `allure-results/` as `allure-results.zip`
   - Available for download from GitHub Actions
   - Passed to Deploy stage
   - **Duration**: ~10-15 seconds

**Job Name**: `test`  
**Runs on**: `ubuntu-latest` (GitHub-hosted runner in cloud)  
**Depends on**: `build` job  
**Parallel Workers**: 12

---

#### **Stage 3: Deploy** 🚀
**Purpose**: Generate HTML reports and publish to GitHub Pages

**Steps**:
1. **Download Test Results**
   - Retrieves `allure-results.zip` from Test stage
   - Extracts JSON results for report generation
   
2. **Setup GitHub Pages**
   - Configures Pages deployment permissions
   - Sets up artifact upload for Pages
   - Uses `actions/configure-pages@v3`
   
3. **Create Root Redirect**
   - Generates `index.html` in root:
     ```html
     <!DOCTYPE html>
     <html>
       <head>
         <meta http-equiv="refresh" content="0; url=/playwright-api-automation-python/allure-report/" />
       </head>
       <body>Redirecting to Allure Report...</body>
     </html>
     ```
   - Enables direct access via root URL
   
4. **Generate Allure HTML Report**
   - Installs Allure commandline tool
   - Runs `allure generate --clean -o allure-report`
   - Creates rich HTML dashboard with:
     - Test suites overview
     - Graphs and charts (duration, status, trends)
     - Timeline view of parallel execution
     - Categorization (features, stories, severity)
     - Detailed test logs with attachments
   
5. **Deploy to GitHub Pages**
   - Uploads `allure-report/` directory
   - Publishes to GitHub Pages
   - **URL**: https://foyezkabir.github.io/playwright-api-automation-python/allure-report
   - Updates immediately (no cache delay)
   - **Duration**: ~3-5 seconds

**Job Name**: `deploy`  
**Runs on**: `ubuntu-latest` (GitHub-hosted runner in cloud)  
**Depends on**: `test` job  
**Deployment**: GitHub Pages

---

### Complete Pipeline Timeline

```mermaid
graph LR
    A[Git Push] --> B[Build Job]
    B --> C[Setup Python 3.12]
    C --> D[Install Dependencies]
    D --> E[Configure .env]
    E --> F[Cache Build]
    F --> G[Test Job]
    G --> H[Run 29 Tests in Parallel]
    H --> I[Generate Allure Results]
    I --> J[Upload Artifacts]
    J --> K[Deploy Job]
    K --> L[Generate HTML Report]
    L --> M[Publish to GitHub Pages]
    M --> N[Live Report Available]
```

**Total Pipeline Duration**: ~18-28 seconds  
**Stages**: 3 (Build → Test → Deploy)  
**Jobs**: 3 (run sequentially with dependency chain)  
**Artifacts**: Build cache + Allure results + HTML report

### Workflow Configuration
**File**: `.github/workflows/api-tests.yml`

**Triggers**:
- ✅ Push to any branch
- ✅ Pull requests
- ✅ Manual workflow dispatch

**Execution Time**: ~15-20 seconds average

### 📊 Viewing Test Reports

#### GitHub Pages (Recommended)
🔗 **Live Report**: https://foyezkabir.github.io/playwright-api-automation-python/allure-report

Features:
- 📈 Test execution trends and history
- 📊 Test duration analytics
- 📋 Categorized test results (Suites, Graphs, Timeline)
- 🎯 Test categorization by features and stories
- 📎 Request/response attachments
- ⚡ Real-time updates after each push

#### GitHub Actions Tab
- View workflow runs and logs
- Download test artifacts (allure-results.zip)
- Monitor pipeline execution status
- Check build/test/deploy stage logs

**To view the deployed report from GitHub Actions:**
1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. Select the latest workflow run (e.g., "API Tests")
4. Scroll down to the **Deploy** job section
5. Look for the **github-pages** deployment in the job summary
6. Click on the deployment URL, or visit: https://foyezkabir.github.io/playwright-api-automation-python/allure-report

---

## 🔌 MCP Servers Integration

This project leverages **Model Context Protocol (MCP)** servers to enhance testing capabilities with browser automation and API validation tools. MCP allows AI assistants to interact with external tools and services seamlessly.

### 🎭 Playwright MCP Server

**Purpose**: Provides browser automation capabilities for UI/UX validation and end-to-end testing.

**What it does:**
- 🌐 **Browser Control** - Launch and control browser instances (Chromium, Firefox, WebKit)
- 🖱️ **Element Interaction** - Click, type, hover, drag-and-drop on web elements
- 📸 **Visual Testing** - Take screenshots and snapshots for validation
- 🔍 **DOM Inspection** - Query and inspect page elements and structure
- 🎯 **Form Automation** - Fill forms, upload files, handle dialogs
- ⏱️ **Wait Conditions** - Wait for elements, text, or network conditions
- 🧪 **Accessibility Testing** - Capture accessibility tree snapshots

**How it works:**
- Runs via `npx @playwright/mcp@latest` (Node.js package)
- Provides tools for browser automation through MCP protocol
- Used for validating actual application behavior vs API responses
- Enables cross-browser testing without writing Playwright scripts

**Use cases in this project:**
- Verifying UI reflects API responses correctly
- Testing scenarios where frontend validation differs from backend
- Discovering API endpoints by inspecting network requests
- Visual regression testing for critical user flows

**Configuration** (`.vscode/mcp.json`):
```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest"],
    "type": "stdio"
  }
}
```

---

### 🛠️ Chrome DevTools MCP Server

**Purpose**: Provides deep browser inspection and debugging capabilities using Chrome DevTools Protocol.

**What it does:**
- 🌍 **Page Management** - Create, navigate, close, and switch between browser tabs
- 🔍 **Network Monitoring** - Capture all HTTP requests/responses, including headers and payloads
- 💻 **JavaScript Execution** - Execute custom scripts in page context
- 📊 **Performance Analysis** - Record performance traces and analyze Core Web Vitals
- 🖥️ **Console Logging** - Capture browser console messages (errors, warnings, logs)
- 📱 **Device Emulation** - Emulate mobile devices, network throttling, geolocation
- 📸 **Advanced Screenshots** - Capture full page or element-specific screenshots
- 🔄 **Real-time Interaction** - Click, fill forms, press keys, handle dialogs

**How it works:**
- Runs via `npx chrome-devtools-mcp@latest` (Node.js package)
- Connects to Chrome/Chromium using DevTools Protocol
- Provides programmatic access to all Chrome DevTools features
- Enables API endpoint discovery through network panel inspection

**Use cases in this project:**
- 🔎 **API Endpoint Discovery** - Used to find the resend OTP endpoint by:
  - Navigating to the application signup page
  - Monitoring network requests in real-time
  - Capturing the exact API endpoint, headers, and payload
  - Analyzing request/response structure
- 🐛 **Debugging** - Inspect JavaScript errors and console logs
- ⚡ **Performance Testing** - Analyze page load times and resource usage
- 🔐 **Security Testing** - Examine request headers, cookies, and authentication flows
- 📱 **Responsive Testing** - Test API integration with different viewport sizes

**Configuration** (`.vscode/mcp.json`):
```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["-y", "chrome-devtools-mcp@latest"]
  }
}
```

---

### 🚀 MCP Workflow in This Project

**Example: Discovering the Resend OTP Endpoint**

1. **Launch Chrome DevTools MCP** - Connect to browser with DevTools Protocol
2. **Navigate to Application** - Open the signup verification page
3. **Trigger Action** - Click "Resend OTP" button on the UI
4. **Capture Network Request** - DevTools MCP captures the API call:
   - Endpoint: `POST /api/authentication/signup/resend-code/`
   - Payload: `{"email": "user@example.com"}`
   - Response: `200 ConfirmationCodeResent`
5. **Create Test Cases** - Use discovered endpoint to write comprehensive tests
6. **Validate Rate Limiting** - Test discovered that API blocks after 5 resend attempts

**Benefits of MCP Integration:**
- ✅ No need to manually inspect Network tab in browser
- ✅ Automated API endpoint discovery
- ✅ AI-assisted test case generation from real application behavior
- ✅ Seamless integration between UI validation and API testing
- ✅ Faster development with context-aware tooling

---

##  API Endpoints Tested

**Base URL**: `https://eks-dev-lb.shadhinlab.xyz`

### 1. Signup API
- **Endpoint**: `POST /api/authentication/signup/`
- **Payload**:
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }
  ```
- **Tests**: 19 (8 passed, 11 xfailed for security issues)

### 2. Email Verification API
- **Endpoint**: `POST /api/authentication/signup/confirm/`
- **Payload**:
  ```json
  {
    "email": "john.doe@example.com",
    "confirmation_code": "123456"
  }
  ```
- **Tests**: 5 (all passed)

### 3. Resend OTP API
- **Endpoint**: `POST /api/authentication/signup/resend-code/`
- **Payload**:
  ```json
  {
    "email": "john.doe@example.com"
  }
  ```
- **Tests**: 5 (all passed)
- **Rate Limiting**: Blocks after 5 resend attempts

## 📊 Test Coverage (29 Total Tests)

### ✅ Signup API Tests (19 tests)
**Passed (8 tests):**
- Valid user registration (200/201)
- Duplicate email handling (409 USERNAME_EXISTS)
- Missing required fields validation (400)
- Invalid email format (400)
- Public domain blocking (gmail, yahoo, hotmail, outlook)

**xfailed (11 tests) - Security Issues Documented:**
- Name validation bypass (API accepts invalid names when frontend bypassed)
- Password complexity bypass (API crashes with 500 error)
- These tests document scenarios where **frontend validation can be bypassed** (Postman, curl, etc.)

### ✅ Email Verification Tests (5 tests - all passed)
- Valid 6-digit OTP verification
- Invalid OTP handling (CODE_MISMATCH)
- Expired/non-existent email (404 UserNotFound)
- Incomplete OTP (less than 6 digits)
- Missing confirmation code validation

### ✅ Resend OTP Tests (5 tests - all passed)
- Successful resend (200 ConfirmationCodeResent)
- Missing email validation (400)
- Non-existent email (404)
- Already verified email handling
- Rate limiting after 5 attempts (400/429)

## ⚙️ Setup & Usage

### Prerequisites
- Python 3.12+
- pip
- Virtual environment

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/foyezkabir/playwright-api-automation-python.git
   cd playwright-api-automation-python
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   # Copy example file
   copy .env.example .env
   
   # Edit .env if needed (optional - defaults provided)
   ```

### Running Tests

#### Basic Execution
```bash
# Normal test run (no README update)
pytest tests/ -v

# Run specific test file
pytest tests/test_signup.py
pytest tests/test_signup_verification.py

# Run specific test
pytest tests/test_signup.py::TestSignup::test_signup_success
```

#### Auto-Update README with Test Results 🔄
After every test run, automatically update the README with latest results:

**Method 1: Using --update-readme Flag (Recommended)**
```bash
# Test run with README auto-update
pytest tests/ --update-readme
```

**Method 2: Using Batch Script (Windows)**
```bash
# Runs tests and updates README automatically
docs\run_tests_and_update_readme.bat
```

**Method 3: Using Environment Variable**
```bash
# Set environment variable and run tests
set UPDATE_README=true
pytest tests/

# Or in one line (PowerShell)
$env:UPDATE_README="true"; pytest tests/
```

**Method 4: Manual Update**
```bash
# Run tests first
pytest tests/

# Then manually update README
python sync_readme_test_results.py
```

**How it works:**
- Captures pytest output and statistics
- Parses test counts (passed, failed, xfailed, skipped)
- Extracts execution time
- Updates the "Test Execution Results" section in README
- Adds timestamp of last run

#### With Allure Reports (Local)
```bash
# Generate Allure results
pytest --alluredir=./allure-results

# Serve report locally
allure serve ./allure-results
```

#### Parallel Execution
```bash
# Run with 12 workers (faster)
pytest -n 12

# Auto-detect CPU cores
pytest -n auto
```

#### By Test Category
```bash
# Smoke tests only
pytest -m smoke_test

# Validation tests only
pytest -m validation_test

# Regression suite
pytest -m regression_test
```

#### With Retries
```bash
# Retry failed tests up to 3 times
pytest --reruns 3 --reruns-delay 1
```

### Configuration (.env file)

```bash
# Environment
ENV=dev                          # dev, staging, prod

# API Configuration
BASE_URL=https://eks-dev-lb.shadhinlab.xyz
API_TIMEOUT=30

# Test Execution
RETRY_COUNT=2
PARALLEL_WORKERS=12

# Reporting
ALLURE_RESULTS_DIR=./allure-results
REPORT_PORTAL_ENABLED=false      # ReportPortal removed
```

## 📁 Project Structure

```
.
├── __pycache__/                       # Python compiled bytecode (gitignored)
├── .github/
│   └── workflows/
│       └── api-tests.yml              # CI/CD pipeline (Build→Test→Deploy)
├── .pytest_cache/                     # Pytest cache directory (gitignored)
├── .vscode/                           # VS Code workspace settings
│   ├── mcp.json                       # Model Context Protocol configuration
│   └── settings.json                  # VS Code editor settings
├── allure-results/                    # Allure test execution results (gitignored)
├── apiObjects/                        # API client objects for different features
│   ├── __init__.py                    # Package initialization
│   └── api_objects.py                 # Signup/Verification API clients
├── docs/                              # Project documentation
│   ├── AUTO_UPDATE_README.md          # Guide for auto-updating README with test results
│   └── run_tests_and_update_readme.bat # Batch script to run tests and sync results
├── logs/                              # Test execution logs (gitignored)
├── screenshots/                       # Test failure screenshots (gitignored)
├── tests/                             # Test modules organized by feature
│   ├── __init__.py                    # Package initialization
│   ├── test_signup.py                 # Signup API tests (19 tests)
│   └── test_signup_verification.py    # Verification + Resend OTP tests (10 tests)
├── venv/                              # Python virtual environment (gitignored)
├── .env                               # Environment variables (gitignored - local only)
├── .env.example                       # Example environment variables template
├── .gitignore                         # Git ignore patterns
├── api_objects.py                     # API client with helper methods
├── config.py                          # Environment configuration management
├── conftest.py                        # Pytest fixtures & configuration
├── data_factory.py                    # Test data generation (Faker)
├── decorators.py                      # Custom decorators (13+ decorators)
├── pytest.ini                         # Pytest configuration
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── schemas.py                         # Pydantic models for validation
├── setup.py                           # Package installation configuration
└── sync_readme_test_results.py        # Script to sync test results to README
```

## 🎨 Custom Decorators

Located in `decorators.py` - 13+ decorators for test organization:

```python
@api_smoke(method="POST", endpoint="/api/authentication/signup/")
def test_signup_success(self, signup_api):
    """Critical smoke test for signup API"""
    pass

@validation_test(field="email", validation_type="format")
def test_invalid_email_format(self, signup_api):
    """Field-level validation test"""
    pass

@known_bug(bug_id="BUG-001", reason="API returns 500 for weak passwords")
def test_password_complexity(self, signup_api):
    """xfail test documenting known issue"""
    pass

@regression_test(title="Test duplicate email", severity="CRITICAL")
def test_duplicate_email(self, signup_api):
    """Regression test with severity"""
    pass

@feature_story(feature='Authentication', story='Signup Verification')
class TestSignupVerification:
    """Test suite with Allure categorization"""
    pass
```

## 🛠️ Advanced Features

### Test Data Factory
```python
from data_factory import UserDataFactory

# Generate unique test data
payload = UserDataFactory.create_signup_payload()
# Output: {name: "User 1736153695", email: "user_1736153695123@example.com", password: "Password123!"}

# Custom data
payload = UserDataFactory.create_signup_payload(
    name="John Doe",
    email="custom@example.com"
)
```

### API Client Helper Methods
```python
# In api_objects.py - SignupClient class

# Basic API calls
response = signup_api.create_user(payload)
response = signup_api.confirm_signup(verification_payload)
response = signup_api.resend_confirmation_code(resend_payload)

# Helper method for rate limit testing
result = signup_api.test_resend_rate_limit(email="test@example.com", max_attempts=5)
# Returns: {"successful_attempts": 5, "blocked_response": APIResponse}

# Utility methods
email = SignupClient.generate_unique_email(prefix="test")
payload = SignupClient.default_payload(email_prefix="user")
```

### Browser Validation (Chrome DevTools MCP)
Used for verifying actual UI behavior vs API behavior:
- Navigate to live application
- Inspect UI elements and structure
- Capture network requests and responses
- Validate frontend validation rules
- Screenshot evidence of UI state

## 🐛 Critical Findings & Security Issues

### ⚠️ API Security Vulnerabilities

**1. Name Validation Missing** (11 xfailed tests)
- Frontend validates name format, but API accepts:
  - Names with numbers: "User123" → 201 ✅ (should be 400 ❌)
  - Special characters: "@User", "User!" → 201 ✅
  - Too short: "Ab" → 201 ✅
  - Leading/trailing spaces: " User " → 201 ✅
- **Risk**: Data integrity issues, potential injection attacks
- **Tests**: `test_signup_name_validation_failures` (7 parameterized tests)

**2. Password Complexity Causes Server Crash** (4 xfailed tests)
- Weak passwords cause API to return **500 Internal Server Error**:
  - Missing uppercase: "password123!" → 500 💥
  - Missing lowercase: "PASSWORD123!" → 500 💥
  - Missing number: "Password!" → 500 💥
  - Missing special char: "Password123" → 500 💥
- **Risk**: Server instability, poor user experience
- **Tests**: `test_signup_password_complexity` (4 parameterized tests)

**3. Public Email Domains Blocked** ✅
- API correctly blocks: gmail.com, yahoo.com, hotmail.com, outlook.com
- Returns 400 with proper error message
- **Tests**: `test_signup_email_public_domain` (4 tests, all passing)

**Note**: All xfailed tests document scenarios where **frontend validation can be bypassed** using tools like Postman, curl, or direct API calls. These represent real security vulnerabilities that should be fixed with server-side validation.

## 📈 Test Execution Results

### Latest Test Run (2026-01-06 11:36:07)
```
========================== test session starts ==========================
collected 29 items

test_signup.py                                     19 tests
  ✅ 18 passed
  ⚠️ 11 xfailed (security issues documented)

test_signup_verification.py                        10 tests
  ✅ 10 passed

==================== 18 passed, 11 xfailed in N/As ====================
```

### Performance Metrics
- **Total Tests**: 29
- **Execution Time**: ~N/A seconds
- **Parallel Workers**: 12
- **Retry Attempts**: Up to 3 per test
- **CI/CD Pipeline**: ~15-20 seconds total
- **Last Updated**: 2026-01-06 11:36:07
## 🤝 Contributing

Contributions welcome! Please follow these steps:

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
- Allure Framework for beautiful test reports
- GitHub Actions for seamless CI/CD
- Open Source Community

---

**⭐ Star this repository if you find it helpful!**

**📊 View Live Reports**: https://foyezkabir.github.io/playwright-api-automation-python/allure-report
