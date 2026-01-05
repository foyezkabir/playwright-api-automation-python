# 🚀 ReportPortal Setup Guide

## What is ReportPortal?

**ReportPortal** is an open-source AI-powered test automation dashboard that provides:
- 🤖 **AI-powered test analysis** - Automatically categorizes failures
- 📊 **Real-time test reporting** - Live dashboard during test execution
- 📈 **Advanced analytics** - Trends, patterns, and insights
- 🔍 **Smart defect triage** - ML-based failure analysis
- 📸 **Rich attachments** - Screenshots, logs, videos
- 🔗 **Integrations** - Jira, Slack, email notifications

---

## 🛠️ Installation Options

### Option 1: Docker (Recommended)

1. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop

2. **Pull and Run ReportPortal**
   ```powershell
   # Download docker-compose file
   curl -LO https://raw.githubusercontent.com/reportportal/reportportal/master/docker-compose.yml
   
   # Start ReportPortal
   docker-compose -p reportportal up -d
   
   # Check status
   docker-compose -p reportportal ps
   ```

3. **Access ReportPortal UI**
   - Open browser: http://localhost:8080
   - Default credentials:
     - Username: `superadmin`
     - Password: `erebus`

### Option 2: Kubernetes
   ```bash
   helm repo add reportportal https://reportportal.io/kubernetes
   helm install reportportal reportportal/reportportal
   ```

### Option 3: Cloud Hosted
   - Use ReportPortal.io SaaS: https://reportportal.io/

---

## ⚙️ Configuration Steps

### Step 1: Create Project in ReportPortal

1. Login to ReportPortal UI (http://localhost:8080)
2. Click **Add Project**
3. Project Name: `api_automation`
4. Click **Create**

### Step 2: Get API Token

1. Click on your **profile icon** (top-right)
2. Go to **Profile** → **API Keys**
3. Copy your **UUID token**

### Step 3: Configure Environment Variables

Create/update `.env` file:
```env
REPORT_PORTAL_ENABLED=true
RP_ENDPOINT=http://localhost:8080
RP_PROJECT=api_automation
RP_UUID=your-uuid-token-here
RP_LAUNCH_NAME=API Automation Tests
```

### Step 4: Install Dependencies

```powershell
pip install pytest-reportportal
```

### Step 5: Update pytest.ini

Ensure your [pytest.ini](pytest.ini) has ReportPortal configuration:
```ini
[pytest]
addopts = --reportportal
```

---

## 🎯 Running Tests with ReportPortal

### Basic Execution
```powershell
pytest test_signup.py --reportportal
```

### With Custom Launch Name
```powershell
$env:RP_LAUNCH_NAME="Signup API Regression"
pytest test_signup.py --reportportal
```

### Parallel Execution with ReportPortal
```powershell
pytest test_signup.py -n 4 --reportportal
```

---

## 📊 Viewing Results

1. **Open ReportPortal UI:** http://localhost:8080
2. **Navigate to:** Launches → `api_automation`
3. **View:**
   - ✅ Test execution status
   - ⏱️ Duration and trends
   - 📋 Detailed logs
   - 📸 Screenshots and attachments
   - 🤖 AI-powered failure analysis

---

## 🤖 AI-Powered Features

### Auto Analysis
ReportPortal's AI engine automatically:
- Identifies similar failures across runs
- Suggests defect types (Product Bug, Automation Bug, System Issue)
- Groups related failures
- Provides failure patterns and trends

### Enable Auto Analysis:
1. Go to **Project Settings**
2. Enable **Auto-Analysis**
3. Choose analysis mode:
   - **Launch Names** - Compares with launches with same name
   - **All Launches** - Compares with all historical data

### Pattern Analysis
ReportPortal ML identifies:
- Flaky tests
- Environment-related failures
- Recurring issues
- New vs. known failures

---

## 🔗 Integrations

### Jira Integration
1. Go to **Project Settings** → **Integrations**
2. Add **Jira**
3. Enter Jira URL, username, API token
4. Post defects directly from ReportPortal to Jira

### Slack Notifications
1. Go to **Project Settings** → **Notifications**
2. Add **Slack**
3. Enter webhook URL
4. Configure notification rules

### Email Notifications
1. Go to **Project Settings** → **Notifications**
2. Add **Email**
3. Configure rules (on launch finish, on failure, etc.)

---

## 📝 Advanced Usage

### Custom Attributes
```python
from reportportal_helpers import ReportPortalHelper

# Add custom attributes
ReportPortalHelper.add_attributes(
    environment="dev",
    browser="chrome",
    api_version="v1"
)
```

### Log API Requests
```python
ReportPortalHelper.log_request(
    test_name="test_signup_success",
    method="POST",
    url="/api/authentication/signup/",
    payload={"name": "Test User", "email": "test@example.com"}
)
```

### Attach Screenshots
```python
ReportPortalHelper.add_screenshot(
    screenshot_path="./screenshots/failure.png",
    description="Error Screenshot"
)
```

### Report Bugs
```python
ReportPortalHelper.log_bug(
    bug_id="BUG-123",
    description="Password validation returns 500 error",
    severity="CRITICAL"
)
```

---

## 📈 Best Practices

1. **Use Consistent Launch Names** - Helps AI analysis compare results
2. **Add Rich Logs** - Include request/response data for debugging
3. **Tag Tests Properly** - Use markers (smoke, regression, etc.)
4. **Enable Auto-Analysis** - Let AI categorize failures
5. **Review Defects Daily** - Triage and analyze patterns
6. **Set Up Notifications** - Get alerted on critical failures
7. **Use Nested Steps** - Structure complex test flows

---

## 🔧 Troubleshooting

### Tests Not Appearing in ReportPortal
- Check `RP_ENDPOINT` is correct
- Verify `RP_UUID` token is valid
- Ensure `pytest-reportportal` is installed
- Check ReportPortal is running: `docker-compose ps`

### Connection Errors
```powershell
# Check if ReportPortal is accessible
curl http://localhost:8080/api/v1/
```

### Docker Issues
```powershell
# Restart containers
docker-compose -p reportportal restart

# View logs
docker-compose -p reportportal logs -f
```

---

## 📚 Resources

- **Official Docs:** https://reportportal.io/docs/
- **GitHub:** https://github.com/reportportal
- **Installation Guide:** https://reportportal.io/installation
- **Integration Guide:** https://reportportal.io/docs/log-data-in-reportportal/test-framework-integration/Python/pytest
- **Community:** https://reportportal.io/community

---

## 🎓 Quick Start Video

Watch the setup tutorial: https://www.youtube.com/watch?v=CpF_5q7H_Ts

---

**Need Help?** Check our [TEST_COVERAGE.md](TEST_COVERAGE.md) for test execution details or raise an issue in the repository.
