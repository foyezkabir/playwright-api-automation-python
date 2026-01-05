# GitHub Actions Secrets Configuration Guide

This guide explains how to configure GitHub Secrets for your CI/CD pipeline.

## 📍 Accessing Secrets Settings

1. Go to your GitHub repository
2. Click **Settings** tab
3. Navigate to **Secrets and variables** → **Actions**
4. Click **New repository secret**

---

## 🔑 Required Secrets

### BASE_URL
- **Description:** API base URL for testing
- **Example:** `https://eks-dev-lb.shadhinlab.xyz`
- **Required:** Yes
- **Used in:** All test executions

### RP_ENABLED
- **Description:** Enable/disable ReportPortal integration
- **Example:** `true` or `false`
- **Configuration:** Go to Settings → Secrets and variables → Actions → **Variables** tab (NOT Secrets)
- **Note:** This should be a **Repository Variable**, not a secret, so it can be checked in workflow conditions
- **Required:** No (defaults to false)
- **Used in:** ReportPortal reporting

### RP_ENDPOINT
- **Description:** ReportPortal server URL
- **Example:** `http://reportportal.example.com:8080`
- **Required:** Only if RP_ENABLED=true
- **Used in:** ReportPortal connection

### RP_PROJECT
- **Description:** ReportPortal project name
- **Example:** `api_automation`
- **Required:** Only if RP_ENABLED=true
- **Used in:** ReportPortal project identification

### RP_UUID
- **Description:** ReportPortal API token (UUID)
- **How to get:**
  1. Login to ReportPortal
  2. Click profile icon
  3. Go to Profile → API Keys
  4. Copy UUID token
- **Example:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Required:** Only if RP_ENABLED=true
- **Used in:** ReportPortal authentication
- **Security:** Keep this secret!

---

## 📝 Step-by-Step Setup

### 1. Create BASE_URL Secret
```
Name: BASE_URL
Value: https://eks-dev-lb.shadhinlab.xyz
```

### 2. Create ReportPortal Configuration (Optional)

**Important:** `RP_ENABLED` should be a **Variable**, not a Secret!

**Step 2a: Create Repository Variable for RP_ENABLED**
1. Go to Settings → Secrets and variables → Actions
2. Click on **Variables** tab (NOT Secrets tab)
3. Click **New repository variable**
4. Add:
```
Name: RP_ENABLED
Value: true
```

**Step 2b: Create Secrets for RP credentials**
1. Go back to **Secrets** tab
2. Add the following secrets:

```
Name: RP_ENDPOINT
Value: http://your-reportportal-server:8080
```

```
Name: RP_PROJECT
Value: api_automation
```

```
Name: RP_UUID
Value: your-uuid-token-from-reportportal
```

---

## 🔒 Security Best Practices

1. **Never commit secrets to code**
   - Use GitHub Secrets for sensitive data
   - Never put tokens in .env files that are committed

2. **Rotate secrets regularly**
   - Change API tokens periodically
   - Update secrets in GitHub when rotated

3. **Use environment-specific secrets**
   - Different secrets for dev/staging/prod
   - Use environment protection rules

4. **Limit secret access**
   - Only give access to necessary workflows
   - Review secret usage regularly

5. **Audit secret usage**
   - Check workflow logs for secret leaks
   - Monitor access patterns

---

## ✅ Verification

After adding secrets, verify they work:

1. **Go to Actions tab**
2. **Manually trigger workflow:**
   - Click on "API Test Automation" workflow
   - Click "Run workflow"
   - Select environment
   - Click "Run workflow"

3. **Check workflow execution:**
   - Verify no errors related to missing secrets
   - Check that ReportPortal uploads (if enabled)
   - Verify Slack notifications (if enabled)

---

## 🔧 Troubleshooting

### Secret not found error
```
Error: Secret BASE_URL not found
```
**Solution:** Ensure secret name matches exactly (case-sensitive)

### Invalid ReportPortal credentials
```
Error: ReportPortal authentication failed
```
**Solution:**
- Verify RP_UUID is correct
- Check RP_ENDPOINT is accessible
- Ensure RP_PROJECT exists in ReportPortal

---

## 📚 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [ReportPortal API Tokens](https://reportportal.io/docs/authorization)

---

## 🌐 Environment-Specific Configuration

### Using Different Secrets per Environment

GitHub Actions supports environment-specific secrets:

1. **Create Environments:**
   - Go to Settings → Environments
   - Create: `development`, `staging`, `production`

2. **Add Environment Secrets:**
   - Click on environment
   - Add secrets specific to that environment

3. **Reference in Workflow:**
   ```yaml
   jobs:
     test:
       environment: development  # or staging, production
       steps:
         - name: Run tests
           env:
             BASE_URL: ${{ secrets.BASE_URL }}  # Uses environment-specific secret
   ```

---

## 📋 Quick Checklist

Before running your pipeline, ensure:

- [ ] BASE_URL secret is configured
- [ ] If using ReportPortal:
  - [ ] RP_ENABLED is set to `true`
  - [ ] RP_ENDPOINT is configured
  - [ ] RP_PROJECT is configured
  - [ ] RP_UUID is configured
- [ ] All secret names match exactly (case-sensitive)
- [ ] Secrets are available in the repository/environment scope

---

**Ready to run?** Trigger your workflow and watch the magic happen! 🚀
