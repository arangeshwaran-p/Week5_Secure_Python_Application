"""Password hashing helpers using PBKDF2-HMAC-SHA256."""
import hashlib
import hmac
import secrets

ITERATIONS = 600_000
SALT_BYTES = 16
HASH_BYTES = 32

def hash_password(password):
    salt = secrets.token_bytes(SALT_BYTES)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS, dklen=HASH_BYTES
    )
    return salt.hex(), derived.hex()

def verify_password(password, salt_hex, expected_hash_hex):
    try:
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(expected_hash_hex)
    except (TypeError, ValueError):
        return False
    if len(salt) != SALT_BYTES or len(expected) != HASH_BYTES:
        return False
    actual = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS, dklen=HASH_BYTES
    )
    return hmac.compare_digest(actual, expected)
