# 🚀 Getting Started Guide

Welcome to the API Test Automation Framework! This guide will help you get up and running quickly.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.8+** installed
- ✅ **Git** installed
- ✅ **Docker Desktop** (optional, for ReportPortal)
- ✅ **Code editor** (VS Code recommended)

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Clone & Setup
```powershell
# Clone the repository
git clone https://github.com/foyezkabir/playwright-api-automation-python.git
cd playwright-api-automation-python

# Run automated setup (installs everything!)
python setup.py
```

The setup script will:
- ✓ Check Python version
- ✓ Install all dependencies
- ✓ Install Playwright browsers
- ✓ Create .env configuration file
- ✓ Create necessary directories
- ✓ Verify installation

### Step 2: Run Tests
```powershell
# Run all tests
pytest

# Or run with all features enabled
pytest -n auto --alluredir=./allure-results
```

### Step 3: View Results
```powershell
# Generate and view Allure report
allure serve ./allure-results
```

**That's it!** Your first test run is complete! 🎉

---

## 📖 Detailed Setup

### Manual Installation (Alternative)

If you prefer manual setup:

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Configure environment
copy .env.example .env
# Edit .env with your settings
```

---

## ⚙️ Configuration

### Basic Configuration

Edit the `.env` file:

```env
# Minimal configuration for local testing
ENV=dev
BASE_URL=https://eks-dev-lb.shadhinlab.xyz
RETRY_COUNT=2
PARALLEL_WORKERS=4
```

### Advanced Configuration (Optional)

```env
# Enable Allure reporting
ALLURE_RESULTS_DIR=./allure-results

# Enable ReportPortal (AI-powered analytics)
REPORT_PORTAL_ENABLED=true
RP_ENDPOINT=http://localhost:8080
RP_PROJECT=api_automation
RP_UUID=your-uuid-here

# Enable Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## 🧪 Running Tests

### Basic Commands

```powershell
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_signup.py

# Run specific test
pytest test_signup.py::TestSignup::test_signup_success
```

### Advanced Execution

```powershell
# Parallel execution (fast!)
pytest -n auto

# With auto-retry for flaky tests
pytest --reruns 2

# Generate Allure report
pytest --alluredir=./allure-results
allure serve ./allure-results

# Run only smoke tests
pytest -m smoke

# Run everything (parallel + retry + reports)
pytest -n auto --reruns 2 --alluredir=./allure-results
```

---

## 📊 Viewing Reports

### Option 1: Allure Report (Recommended)

```powershell
# Generate results during test run
pytest --alluredir=./allure-results

# View interactive report
allure serve ./allure-results

# Or generate static HTML
allure generate ./allure-results -o ./allure-report
# Then open: allure-report/index.html
```

**Allure Report Features:**
- 📈 Test execution timeline
- 📊 Pass/fail statistics  
- 🔍 Detailed error traces
- 📸 Screenshots (if added)
- 📋 Request/response logs
- 📉 Historical trends

### Option 2: ReportPortal (AI-Powered)

```powershell
# 1. Start ReportPortal with Docker
docker-compose up -d

# 2. Access UI at http://localhost:8080
# Login: superadmin / erebus

# 3. Configure .env
# Set: REPORT_PORTAL_ENABLED=true
#      RP_UUID=your-token-here

# 4. Run tests
pytest --reportportal
```

**ReportPortal Features:**
- 🤖 AI-powered failure analysis
- 📊 Real-time dashboard
- 🔍 Smart defect triage
- 📈 Advanced analytics
- 🔗 Jira/Slack integration

See [REPORTPORTAL_SETUP.md](REPORTPORTAL_SETUP.md) for detailed setup.

---

## 📁 Project Structure

```
├── .github/workflows/     # CI/CD pipelines
├── test_signup.py         # Test cases
├── api_objects.py         # API client
├── conftest.py            # Pytest fixtures
├── config.py              # Configuration
├── data_factory.py        # Test data generation
├── schemas.py             # API validation schemas
├── reportportal_helpers.py # RP utilities
├── pytest.ini             # Pytest config
├── requirements.txt       # Dependencies
├── .env                   # Your configuration
└── setup.py               # Automated setup
```

---

## 🎓 Learning Path

### Day 1: Basic Testing
1. ✅ Run `python setup.py`
2. ✅ Run first test: `pytest test_signup.py`
3. ✅ View Allure report
4. ✅ Read [README.md](../README.md)

### Day 2: Advanced Features
1. ✅ Try parallel execution: `pytest -n auto`
2. ✅ Use data factory in tests
3. ✅ Add schema validation
4. ✅ Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### Day 3: Reporting & CI/CD
1. ✅ Setup ReportPortal (optional)
2. ✅ Configure GitHub Actions
3. ✅ Setup Slack notifications
4. ✅ Read [TEST_COVERAGE.md](TEST_COVERAGE.md)

---

## 💡 Common Tasks

### Adding a New Test

```python
import pytest
import allure
from data_factory import UserDataFactory
from schemas import assert_response_schema, SignupSuccessResponseSchema

@allure.feature('Authentication')
@allure.story('Signup')
class TestSignup:
    
    @allure.title("Test successful signup")
    @pytest.mark.smoke
    def test_signup_success(self, signup_api):
        # Generate test data
        payload = UserDataFactory.create_signup_payload()
        
        # Execute API call
        with allure.step("Send signup request"):
            response = signup_api.create_user(payload)
        
        # Validate response
        with allure.step("Verify status code"):
            assert response.status == 201
        
        # Validate schema
        with allure.step("Validate response schema"):
            assert_response_schema(response.json(), SignupSuccessResponseSchema)
```

### Using Test Data Factory

```python
from data_factory import UserDataFactory

# Valid payload
payload = UserDataFactory.create_signup_payload()

# Custom values
payload = UserDataFactory.create_signup_payload(
    name="John Doe",
    email=UserDataFactory.random_email(domain="example.com")
)

# Invalid payload for negative testing
invalid = UserDataFactory.create_invalid_payload("email", "not-an-email")

# Security testing
from data_factory import AttackVectorFactory
sql_payloads = AttackVectorFactory.sql_injection_payloads()
```

### Changing Environment

```powershell
# Option 1: Edit .env file
# Change: ENV=staging

# Option 2: Set environment variable
$env:ENV="staging"
pytest
```

---

## 🔧 Troubleshooting

### Tests Not Running?

```powershell
# Check pytest can find tests
pytest --collect-only

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Import Errors?

```powershell
# Ensure virtual environment is activated
# Windows:
.\venv\Scripts\activate

# Verify packages installed
pip list
```

### Playwright Errors?

```powershell
# Reinstall browsers
playwright install --force chromium

# Check installation
playwright --version
```

### Allure Not Working?

```powershell
# Install Allure CLI
# Option 1: Windows with Scoop
scoop install allure

# Option 2: Download manually
# https://github.com/allure-framework/allure2/releases

# Verify installation
allure --version
```

---

## 📚 Documentation

Your complete documentation library:

- 📖 [README.md](../README.md) - Main documentation
- 🚀 [GETTING_STARTED.md](GETTING_STARTED.md) - This file
- ⚡ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands
- 📊 [TEST_COVERAGE.md](TEST_COVERAGE.md) - Coverage matrix
- 🤖 [REPORTPORTAL_SETUP.md](REPORTPORTAL_SETUP.md) - RP setup
- 🔑 [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) - CI/CD secrets
- 📝 [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What's included

---

## 🎯 Next Steps

After completing this guide:

1. ✅ **Read Quick Reference**
   - Bookmark [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
   - Learn common commands

2. ✅ **Explore Test Coverage**
   - Review [TEST_COVERAGE.md](TEST_COVERAGE.md)
   - Understand what's tested

3. ✅ **Setup CI/CD**
   - Configure GitHub Secrets
   - Push to trigger pipeline

4. ✅ **Try ReportPortal**
   - Follow [REPORTPORTAL_SETUP.md](REPORTPORTAL_SETUP.md)
   - Experience AI-powered analytics

5. ✅ **Write New Tests**
   - Use data factory
   - Add schema validation
   - Log to ReportPortal

---

## 🆘 Getting Help

- 📖 Check documentation files
- 🔍 Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 💬 Open an issue on GitHub
- 📧 Contact the team

---

## ✨ Pro Tips

💡 **Speed Up Tests**
```powershell
pytest -n auto  # 60-70% faster!
```

💡 **Debug Failures**
```powershell
pytest -s -v --tb=short  # Detailed output
```

💡 **Run Smoke Tests Only**
```powershell
pytest -m smoke  # Quick validation
```

💡 **View Test Coverage**
```powershell
pytest --cov=. --cov-report=html
```

---

**Ready to test?** Run `pytest` and start automating! 🚀

---

*Last updated: January 5, 2026*
