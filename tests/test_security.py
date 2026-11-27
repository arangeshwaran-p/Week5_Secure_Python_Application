import tempfile
import unittest
from pathlib import Path
from app import SecureUserApp
from security import hash_password, verify_password
from validation import validate_username, validate_password

class PasswordTests(unittest.TestCase):
    def test_same_password_gets_different_salts(self):
        salt1, hash1 = hash_password("StrongPassword!123")
        salt2, hash2 = hash_password("StrongPassword!123")
        self.assertNotEqual(salt1, salt2)
        self.assertNotEqual(hash1, hash2)

    def test_password_verification(self):
        salt, digest = hash_password("StrongPassword!123")
        self.assertTrue(verify_password("StrongPassword!123", salt, digest))
        self.assertFalse(verify_password("WrongPassword!123", salt, digest))

    def test_malformed_hash_is_rejected(self):
        self.assertFalse(verify_password("anything", "bad", "bad"))

class ValidationTests(unittest.TestCase):
    def test_username_validation(self):
        self.assertEqual(validate_username("student_01"), "student_01")
        with self.assertRaises(ValueError):
            validate_username("x'; DROP TABLE users;--")

    def test_weak_password_rejected(self):
        with self.assertRaises(ValueError):
            validate_password("password")

class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = SecureUserApp(str(Path(self.temp.name) / "test.db"))

    def tearDown(self):
        self.app.close()
        self.temp.cleanup()

    def test_register_and_login(self):
        self.assertTrue(self.app.register("student_01", "StrongPassword!123"))
        self.assertTrue(self.app.login("student_01", "StrongPassword!123"))
        self.assertFalse(self.app.login("student_01", "WrongPassword!123"))

    def test_duplicate_registration_rejected(self):
        self.app.register("student_01", "StrongPassword!123")
        with self.assertRaises(RuntimeError):
            self.app.register("student_01", "AnotherStrong!456")

    def test_sql_injection_username_is_rejected(self):
        with self.assertRaises(ValueError):
            self.app.login("' OR 1=1 --", "anything")

if __name__ == "__main__":
    unittest.main()
