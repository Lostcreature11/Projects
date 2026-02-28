 Secure CLI Password Manager

 Overview
A command-line password manager built with Python that securely stores website credentials using strong encryption.

Credentials are encrypted using AES-GCM, and the encryption key is derived from a master password using PBKDF2 with SHA-256.

---

Features
- Master password protection
- AES-GCM encryption
- PBKDF2 key derivation (480,000 iterations)
- Add credentials
- View stored credentials
- List saved websites
- Encrypted local vault storage

---

Technologies
- Python 3.x
- cryptography library
- JSON
- Base64 encoding

---

 Installation

1. Install Python 3.x  
2. Install required dependency:
