"""Strict validation for user-controlled registration and login fields."""
import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,24}$")

def validate_username(username):
    if not isinstance(username, str) or not USERNAME_RE.fullmatch(username):
        raise ValueError("Username must be 3-24 characters: letters, numbers, underscore.")
    return username

def validate_password(password):
    if not isinstance(password, str):
        raise ValueError("Password must be text.")
    if len(password) < 12:
        raise ValueError("Password must contain at least 12 characters.")
    if len(password) > 128:
        raise ValueError("Password must not exceed 128 characters.")
    if not any(ch.islower() for ch in password):
        raise ValueError("Password must include a lowercase letter.")
    if not any(ch.isupper() for ch in password):
        raise ValueError("Password must include an uppercase letter.")
    if not any(ch.isdigit() for ch in password):
        raise ValueError("Password must include a number.")
    if not any(not ch.isalnum() for ch in password):
        raise ValueError("Password must include a special character.")
    return password
