# 🔐 CryptoLab - CI/CD Pipeline Demo

A Django web application featuring 18 classical and modern cryptographic ciphers, designed as a demo project for CI/CD pipeline implementation.

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/cicd-crypto/actions/workflows/ci.yml/badge.svg)

## 🎯 Features

<<<<<<< Updated upstream
- **11 Classical Ciphers**: Caesar, Vigenère, Autokey, One-Time Pad, Hill, Affine, Multiplicative, Playfair, Vernam, Rail Fence, Columnar Transposition
- **Modern UI**: Dark theme with animated background
- **Encrypt & Decrypt**: Full bidirectional support
- **Educational**: Step-by-step examples for each cipher
- **Security Ratings**: Visual strength indicators for measurement purposes
=======
### Classical Ciphers (12)
- **Caesar** - Simple letter shift
- **Additive** - Modular addition cipher
- **Multiplicative** - Modular multiplication cipher
- **Affine** - Combines multiplicative and additive
- **Vigenère** - Polyalphabetic substitution
- **Hill** - Matrix-based encryption
- **Autokey** - Self-extending key cipher
- **Playfair** - Digraph substitution
- **One-Time Pad** - Theoretically unbreakable
- **Vernam** - XOR-based cipher
- **Rail Fence** - Zigzag transposition
- **Columnar Transposition** - Column-based rearrangement

### Modern Ciphers (4)
- **Feistel** - Block cipher structure
- **DES** - Data Encryption Standard
- **AES** - Advanced Encryption Standard
- **RSA** - Asymmetric public-key encryption

### Hash Functions (2)
- **Hashing** - MD5, SHA-1, SHA-256, SHA-512
- **SHA-1** - Dedicated SHA-1 hasher
>>>>>>> Stashed changes

## 🚀 CI/CD Pipeline

| Stage | Tool | Status |
|-------|------|--------|
| Unit Testing | pytest | ✅ Active |
| Code Coverage | pytest-cov | ✅ Active |
| Quality Analysis | SonarCloud | ✅ Active |

## 📋 Quick Start

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/cicd-crypto.git
cd cicd-crypto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python manage.py runserver
# Visit http://127.0.0.1:8000

# Run tests
pytest
pytest --cov=cryptolab --cov-report=html
```

## 🔧 GitHub Setup

### 1. Add Repository Secret
Go to Settings → Secrets → Actions → New repository secret:
- Name: `SONAR_TOKEN`
- Value: Your SonarCloud token

### 2. Update SonarCloud Config
Edit `sonar-project.properties`:
```properties
sonar.organization=your-github-username
sonar.projectKey=your-github-username_cicd-crypto
```

### 3. Branch Protection (Optional)
Settings → Branches → Add rule for `main`:
- ✅ Require status checks: `Unit Tests`, `SonarCloud Analysis`

## 📁 Project Structure

```
cicd-crypto/
├── .github/workflows/ci.yml    # CI/CD pipeline
├── cryptolab/
│   ├── ciphers/                # All cipher implementations
│   │   ├── caesar.py
│   │   ├── aes.py
│   │   ├── rsa.py
│   │   └── ... (18 ciphers)
│   ├── templates/index.html    # Web UI
│   ├── views.py
│   └── settings.py
├── tests/
│   ├── test_ciphers.py         # 61 unit tests
│   └── conftest.py
├── requirements.txt
├── pytest.ini
└── sonar-project.properties
```

## 🧪 Test Coverage

All 18 ciphers have comprehensive tests verifying:
- Encryption functionality
- Decryption functionality  
- Encrypt-decrypt roundtrip
- Key validation
- Edge cases

---
Built for learning CI/CD pipelines 🎓
