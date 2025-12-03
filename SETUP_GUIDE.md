# 🚀 Setup Guide: GitHub Repository & CI/CD Pipeline

This guide walks you through setting up the `cicd-crypto` repository with branch protection and SonarCloud integration.

## Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `cicd-crypto`
3. Description: "CI/CD Pipeline Demo with Classical Cipher Web App"
4. Keep it **Public** (required for free SonarCloud)
5. **DON'T** initialize with README (we have one)
6. Click "Create repository"

## Step 2: Push Code to GitHub

```bash
# Navigate to project folder
cd cicd-crypto

# Initialize git
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: CryptoLab Django app with pytest"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cicd-crypto.git

# Push to main
git branch -M main
git push -u origin main
```

## Step 3: Set Up SonarCloud

### 3.1 Create SonarCloud Account
1. Go to [sonarcloud.io](https://sonarcloud.io)
2. Click "Log in" → "Log in with GitHub"
3. Authorize SonarCloud

### 3.2 Import Your Repository
1. Click the "+" icon → "Analyze new project"
2. Select your GitHub organization
3. Find and select `cicd-crypto`
4. Click "Set Up"

### 3.3 Get Your Configuration Values
After setup, SonarCloud will show you:
- **Organization**: Your GitHub username (e.g., `johnsmith`)
- **Project Key**: `your-username_cicd-crypto`

### 3.4 Update sonar-project.properties
Edit the file and replace the placeholders:
```properties
sonar.organization=YOUR_ACTUAL_GITHUB_USERNAME
sonar.projectKey=YOUR_ACTUAL_GITHUB_USERNAME_cicd-crypto
```

Commit and push:
```bash
git add sonar-project.properties
git commit -m "Configure SonarCloud project"
git push
```

### 3.5 Get SonarCloud Token
1. In SonarCloud, click your profile icon → "My Account"
2. Go to "Security" tab
3. Generate new token: `cicd-crypto-token`
4. **COPY THE TOKEN** (you won't see it again!)

### 3.6 Add Token to GitHub Secrets
1. In GitHub, go to your repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `SONAR_TOKEN`
4. Value: (paste your token)
5. Click "Add secret"

## Step 4: Set Up Branch Protection

1. Go to your repo → Settings → Branches
2. Click "Add branch ruleset" (or "Add rule" for classic protection)

### For Classic Branch Protection:
1. Branch name pattern: `main`
2. Enable these options:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals (set to 1 if working solo, or 0)
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - Search and add: `Unit Tests`
     - Search and add: `SonarCloud Analysis`
   - ✅ **Do not allow bypassing the above settings** (optional)
3. Click "Create" / "Save changes"

### For Rulesets (newer GitHub UI):
1. Ruleset name: `main-protection`
2. Enforcement status: Active
3. Target branches: Add `main`
4. Rules:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass
     - Add: `Unit Tests`, `SonarCloud Analysis`
5. Click "Create"

## Step 5: Verify Pipeline Works

### 5.1 Trigger the Pipeline
The pipeline runs automatically on push. Check the Actions tab:
1. Go to your repo → Actions
2. You should see a workflow running
3. Wait for both jobs to complete (green checkmarks)

### 5.2 Check SonarCloud Results
1. Go to [sonarcloud.io](https://sonarcloud.io)
2. Navigate to your project
3. You should see quality metrics, coverage, and code analysis

## Step 6: Test Branch Protection

1. Create a feature branch:
```bash
git checkout -b feature/test-protection
echo "# Test" >> test.md
git add test.md
git commit -m "Test branch protection"
git push -u origin feature/test-protection
```

2. Go to GitHub and create a Pull Request
3. You should see status checks running
4. PR cannot be merged until checks pass

## 🎉 Done!

Your CI/CD pipeline is now active with:
- ✅ Automated pytest testing on every push
- ✅ Code coverage reporting
- ✅ SonarCloud quality analysis
- ✅ Branch protection requiring passing checks

## Troubleshooting

### Pipeline Fails with "SONAR_TOKEN not found"
- Make sure you added the secret in GitHub (Step 3.6)
- Secret name must be exactly `SONAR_TOKEN`

### SonarCloud Shows "Project not found"
- Check that `sonar-project.properties` has correct values
- Organization and project key must match exactly

### Status Checks Not Appearing in Branch Protection
- Run the pipeline at least once first
- The check names are: `Unit Tests` and `SonarCloud Analysis`

### Tests Pass Locally but Fail in CI
- Check Python version matches (3.11)
- Ensure all dependencies are in requirements.txt
