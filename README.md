# 🔐 CryptoLab - CI/CD Pipeline Demo

A Django web application for classical cipher encryption, designed as a demo project for CI/CD pipeline implementation.

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/cicd-crypto/actions/workflows/ci.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=YOUR_USERNAME_cicd-crypto&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=YOUR_USERNAME_cicd-crypto)

## 🎯 Features

- **11 Classical Ciphers**: Caesar, Vigenère, Autokey, One-Time Pad, Hill, Affine, Multiplicative, Playfair, Vernam, Rail Fence, Columnar Transposition
- **Modern UI**: Dark theme with animated background
- **Encrypt & Decrypt**: Full bidirectional support
- **Educational**: Step-by-step examples for each cipher
- **Security Ratings**: Visual strength indicators for measurement purposes

## 🚀 CI/CD Pipeline

This project demonstrates a CI/CD pipeline with:

| Stage | Tool | Status |
|-------|------|--------|
| Unit Testing | pytest | ✅ Active |
| Code Coverage | pytest-cov | ✅ Active |
| Quality Analysis | SonarCloud | ✅ Active |
| Containerization | Docker | 🔜 Coming |
| Deployment | Heroku | 🔜 Coming |
| Notifications | Discord | 🔜 Coming |

## 📋 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/cicd-crypto.git
cd cicd-crypto
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000

### 5. Run Tests Locally

```bash
pytest
pytest --cov=cryptolab --cov-report=html  # With coverage
```

## 🔧 GitHub Setup

### Repository Secrets

Add these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

| Secret | Description |
|--------|-------------|
| `SONAR_TOKEN` | Your SonarCloud token |

### Branch Protection Rules

1. Go to Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Select status checks: `Unit Tests`, `SonarCloud Analysis`

## 🌐 SonarCloud Setup

1. Go to [sonarcloud.io](https://sonarcloud.io)
2. Sign in with GitHub
3. Click "+" → "Analyze new project"
4. Select your `cicd-crypto` repository
5. Copy your organization name and project key
6. Update `sonar-project.properties`:
   ```properties
   sonar.organization=your-github-username
   sonar.projectKey=your-github-username_cicd-crypto
   ```
7. Go to your SonarCloud project → Administration → Analysis Method
8. Copy the `SONAR_TOKEN`
9. Add it to GitHub Secrets

## 📁 Project Structure

```
cicd-crypto/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions workflow
├── cryptolab/
│   ├── ciphers/                # Cipher implementations
│   │   ├── __init__.py         # Cipher registry
│   │   ├── base.py             # Base cipher class
│   │   ├── caesar.py
│   │   ├── vigenere.py
│   │   ├── autokey.py
│   │   ├── onetimepad.py
│   │   ├── hill.py
│   │   ├── affine.py
│   │   ├── multiplicative.py
│   │   ├── playfair.py
│   │   ├── vernam.py
│   │   ├── railfence.py
│   │   └── columnar.py
│   ├── templates/
│   │   └── index.html          # Main UI template
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_ciphers.py         # Cipher unit tests
│   └── test_views.py           # View unit tests
├── .gitignore
├── manage.py
├── pytest.ini
├── requirements.txt
└── sonar-project.properties
```

## 🧪 Test Coverage

The project includes comprehensive tests for:

- All 11 cipher encrypt/decrypt functions
- Key validation for each cipher
- Encrypt-decrypt roundtrip verification
- Django views and API endpoints
- Cipher registry functionality

## 📝 License

MIT License - feel free to use this for your own CI/CD learning!

---

Built with ❤️ for learning CI/CD pipelines
