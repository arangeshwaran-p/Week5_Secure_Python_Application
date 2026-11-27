"""Command-line interface for the Secure User Management System."""
from database import Database
from security import hash_password, verify_password
from validation import validate_username, validate_password

class SecureUserApp:
    def __init__(self, db_path="users.db"):
        self.db = Database(db_path)

    def register(self, username, password):
        username = validate_username(username)
        validate_password(password)
        salt, password_hash = hash_password(password)
        return self.db.create_user(username, salt, password_hash)

    def login(self, username, password):
        username = validate_username(username)
        record = self.db.get_user(username)
        # Use a dummy hash path for unknown users to reduce timing differences.
        if record is None:
            verify_password(password, "00" * 16, "00" * 32)
            return False
        return verify_password(password, record["salt"], record["password_hash"])

    def close(self):
        self.db.close()

def main():
    app = SecureUserApp()
    try:
        while True:
            print("\n=== Secure User Management ===")
            print("1. Register\n2. Login\n3. Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                try:
                    username = input("Username: ")
                    password = input("Password: ")
                    app.register(username, password)
                    print("Registration successful.")
                except (ValueError, RuntimeError) as exc:
                    print(f"Registration failed: {exc}")
            elif choice == "2":
                try:
                    username = input("Username: ")
                    password = input("Password: ")
                    print("Login successful." if app.login(username, password)
                          else "Invalid username or password.")
                except ValueError as exc:
                    print(f"Login failed: {exc}")
            elif choice == "3":
                break
            else:
                print("Choose 1, 2, or 3.")
    finally:
        app.close()

if __name__ == "__main__":
    main()
