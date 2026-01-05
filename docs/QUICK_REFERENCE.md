# 🚀 Quick Reference Guide

## Common Commands

### Running Tests

```powershell
# Basic run
pytest

# Verbose output
pytest -v

# Run specific test file
pytest test_signup.py

# Run specific test
pytest test_signup.py::TestSignup::test_signup_success

# Run tests with specific marker
pytest -m smoke
pytest -m regression

# Parallel execution (fast!)
pytest -n auto

# With retry for flaky tests
pytest --reruns 2

# Generate Allure report
pytest --alluredir=./allure-results
allure serve ./allure-results

# With ReportPortal
pytest --reportportal
```

---

## Environment Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Copy environment template
copy .env.example .env
```

---

## Configuration

Edit `.env` file:

```env
# Quick Dev Setup
ENV=dev
BASE_URL=https://eks-dev-lb.shadhinlab.xyz
RETRY_COUNT=2
PARALLEL_WORKERS=4
REPORT_PORTAL_ENABLED=false
```

---

## ReportPortal Quick Start

```powershell
# 1. Start ReportPortal with Docker
docker-compose -p reportportal up -d

# 2. Access UI
# Open: http://localhost:8080
# Login: superadmin / erebus

# 3. Get UUID token from profile

# 4. Update .env
# RP_ENDPOINT=http://localhost:8080
# RP_PROJECT=api_automation
# RP_UUID=your-token-here
# REPORT_PORTAL_ENABLED=true

# 5. Run tests
pytest --reportportal
```

---

## Allure Report

```powershell
# Install Allure (Windows with Scoop)
scoop install allure

# Or download from:
# https://github.com/allure-framework/allure2/releases

# Run tests with Allure
pytest --alluredir=./allure-results

# View report
allure serve ./allure-results

# Generate static report
allure generate ./allure-results -o ./allure-report
```

---

## Troubleshooting

### Tests not running?
```powershell
# Check pytest is finding tests
pytest --collect-only

# Check if fixtures work
pytest --fixtures
```

### Import errors?
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

### Playwright issues?
```powershell
# Reinstall browsers
playwright install --force chromium

# Check browser installation
playwright install --help
```

### ReportPortal not working?
```powershell
# Check ReportPortal is running
curl http://localhost:8080/api/v1/

# Check Docker status
docker-compose -p reportportal ps

# View logs
docker-compose -p reportportal logs -f
```

---

## Test Markers

```python
# In your tests, use markers:
@pytest.mark.smoke       # Quick smoke tests
@pytest.mark.regression  # Full regression
@pytest.mark.security    # Security tests
@pytest.mark.slow        # Slow running tests

# Run specific markers:
pytest -m smoke
pytest -m "smoke or regression"
pytest -m "not slow"
```

---

## Useful Pytest Options

```powershell
# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Show local variables on failure
pytest -l

# Show stdout/print statements
pytest -s

# Re-run only failed tests
pytest --lf

# Show test durations
pytest --durations=10

# Code coverage
pytest --cov=. --cov-report=html
```

---

## CI/CD (GitHub Actions)

### Required Secrets
In GitHub repo settings → Secrets and variables → Actions:

```
BASE_URL              # API base URL
RP_ENABLED           # true or false
RP_ENDPOINT          # http://your-reportportal:8080
RP_PROJECT           # api_automation
RP_UUID              # your-uuid-token
SLACK_WEBHOOK_URL    # Slack webhook (optional)
```

### Manual Workflow Trigger
1. Go to Actions tab
2. Select "API Test Automation" workflow
3. Click "Run workflow"
4. Choose environment (dev/staging/prod)
5. Click "Run workflow"

---

## File Structure Reference

```
test_signup.py           → Test cases
api_objects.py           → API client wrapper
conftest.py              → Pytest fixtures
config.py                → Environment config
data_factory.py          → Test data generation
schemas.py               → Pydantic validation
reportportal_helpers.py  → ReportPortal utilities
pytest.ini               → Pytest configuration
.env                     → Environment variables
```

---

## Resources

- 📚 [Full README](../README.md)
- 📊 [Test Coverage](TEST_COVERAGE.md)
- 🤖 [ReportPortal Setup](REPORTPORTAL_SETUP.md)
- 🌐 [Playwright Docs](https://playwright.dev/python/docs/api-testing)
- 🧪 [Pytest Docs](https://docs.pytest.org/)
- 📈 [Allure Docs](https://docs.qameta.io/allure/)
- 🚀 [ReportPortal Docs](https://reportportal.io/docs/)

---

## Quick Tips

💡 **Best Practices**
- Use `pytest -n auto` for faster execution
- Run `pytest -m smoke` before pushing code
- Check Allure report for detailed failure analysis
- Enable ReportPortal for AI-powered insights
- Review test coverage regularly

⚡ **Performance**
- Parallel execution cuts runtime by 60-70%
- Use `--maxfail=5` to fail fast
- Mark slow tests with `@pytest.mark.slow`

🐛 **Debugging**
- Use `-s` to see print statements
- Use `-l` to see local variables
- Use `--pdb` to drop into debugger on failure
- Check Allure report for screenshots/logs

---

**Need Help?** Open an issue or check the documentation files!
