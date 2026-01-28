# 🔐 CryptoLab

An interactive web application for learning and experimenting with classical and modern cryptographic ciphers.

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://cryptolab-sxo4.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://djangoproject.com)

## ✨ Features

### 🔑 Encryption Tools
Encrypt and decrypt text using **11 classical ciphers**:

| Cipher | Type | Description |
|--------|------|-------------|
| Caesar | Substitution | Simple letter shift |
| Vigenère | Polyalphabetic | Keyword-based substitution |
| Affine | Substitution | Combines multiplication and addition |
| Multiplicative | Substitution | Modular multiplication |
| Autokey | Polyalphabetic | Self-extending key |
| Playfair | Digraph | 5×5 matrix substitution |
| Hill | Matrix | Linear algebra encryption |
| One-Time Pad | Stream | Theoretically unbreakable |
| Vernam | Stream | XOR-based cipher |
| Rail Fence | Transposition | Zigzag pattern |
| Columnar | Transposition | Column rearrangement |

### 📚 Learn Page
Interactive explanations for each cipher with:
- Algorithm breakdown
- Visual examples
- Security strength indicators
- "Try It" buttons linking to the encryption tool

### 🛡️ Security Tools
- **Password Exposure Check**: Verify if your password has appeared in data breaches using the [Have I Been Pwned](https://haveibeenpwned.com/) API with **k-anonymity** (your password is never sent over the network).

### 🎨 Modern UI
- Glassmorphism design with dark theme
- Smooth fade-in animations
- Fully responsive (mobile-friendly)
- Operation history tracking

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/idkjustletmein/cicd-crypto.git
cd cicd-crypto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
python manage.py runserver

# Open http://127.0.0.1:8000 in your browser
```

## 📁 Project Structure

```
cicd-crypto/
├── cryptolab/
│   ├── ciphers/           # Cipher implementations
│   │   ├── caesar.py
│   │   ├── vigenere.py
│   │   ├── hill.py
│   │   └── ... (11 ciphers)
│   ├── templates/
│   │   ├── index.html     # Main encryption tool
│   │   ├── learn.html     # Educational content
│   │   ├── security.html  # Password checker
│   │   └── about.html     # Project info
│   └── views.py           # API endpoints
├── tests/                 # Unit tests
├── requirements.txt
└── manage.py
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=cryptolab --cov-report=html
```

## 🌐 Live Demo

Visit the live application: **[cryptolab-sxo4.onrender.com](https://cryptolab-sxo4.onrender.com)**

## 📄 License

This project is open source and available for educational purposes.

---

Built with ❤️ for cryptography enthusiasts
