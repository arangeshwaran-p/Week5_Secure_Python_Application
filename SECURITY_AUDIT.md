# Security Audit Summary

## Scope
Review of the educational command-line user registration/login application and its SQLite data access.

## Findings and mitigations
1. **Password exposure at rest (High, if stored as plaintext):** Store only a PBKDF2-HMAC-SHA256 derived password hash and a unique random salt. Verification derives the candidate hash and compares it with `hmac.compare_digest`.
2. **SQL injection risk (High, if SQL is assembled from user input):** All database values are passed through SQLite placeholders (`?`) rather than string concatenation.
3. **Unvalidated user input (Medium):** Usernames are restricted to 3–24 ASCII letters, digits, and underscores. Passwords have length and character-class checks.
4. **Account enumeration / verbose authentication errors (Medium):** Login returns the same failure message for an unknown username and an incorrect password. This reduces, but does not eliminate, timing and enumeration risks.
5. **Sensitive information in logs/output (Medium):** The application does not log or print passwords or password hashes.

## Validation
Run `py -m unittest discover -s tests -v`. Tests cover unique salts, correct/incorrect password verification, malformed hashes, input validation, registration/login, duplicate accounts, and SQL-injection-shaped usernames.

## Limitations
This is a local CLI learning project. It has no web server, session cookies, TLS, rate limiting, account lockout, MFA, encrypted database, or formal penetration test. The SQL injection test is a regression test, not proof against every possible attack. Use a production framework and a threat model before deployment.
