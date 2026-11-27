# Week 5 – Security Enhancements in Python Applications
## Secure User Management System

A command-line Python application demonstrating secure registration and login with SQLite.

### Features
- PBKDF2-HMAC-SHA256 password hashing with a unique cryptographically random salt.
- Constant-time digest comparison using `hmac.compare_digest`.
- Parameterized SQL statements.
- Strict username and password validation.
- Generic login failure message.
- Automated unit tests, including invalid-input and SQL-injection-shaped input tests.

### Requirements
- Python 3.10 or later (standard library only).

### Run in VS Code (Windows)
1. Extract the ZIP file.
2. Open the extracted `Week5_Secure_App` folder in VS Code.
3. Open Terminal → New Terminal.
4. Run: `py app.py`
5. Run tests: `py -m unittest discover -s tests -v`

If `py` is unavailable, try `python` instead.

### Optional static analysis
Install Bandit: `py -m pip install bandit`
Run: `py -m bandit -r . -x tests`

### Important security notes
- This is an educational local CLI demonstration, not a production-ready web service.
- Do not reuse real passwords or place real personal data in the demo database.
- The app does not encrypt the database file; filesystem permissions and disk encryption are separate controls.
- The test with SQL-injection-shaped input confirms input validation and parameterized-query design; it is not a full penetration test.
- Review `reports/Security_Audit_Report.docx` for scope, findings, limitations, and test instructions.
