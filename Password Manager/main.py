import base64
import hashlib
import os
import secrets
import sqlite3
import string
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken

DB_FILE = "passwords.db"
SALT_FILE = "master.salt"
HASH_FILE = "master.hash"

def derive_key(master_password: str, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac("sha256", master_password.encode(), salt, 200_000, dklen=32)
    return base64.urlsafe_b64encode(key)

def setup_master():
    if os.path.exists(SALT_FILE) and os.path.exists(HASH_FILE):
        return False
    print("First-time setup: create a master password.")
    while True:
        password = getpass("Create master password: ")
        confirm = getpass("Confirm master password: ")
        if len(password) < 8:
            print("Use at least 8 characters.")
        elif password != confirm:
            print("Passwords do not match.")
        else:
            salt = secrets.token_bytes(16)
            digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
            open(SALT_FILE, "wb").write(salt)
            open(HASH_FILE, "wb").write(digest)
            print("Master password created.")
            return True

def authenticate():
    salt = open(SALT_FILE, "rb").read()
    stored = open(HASH_FILE, "rb").read()
    for _ in range(3):
        password = getpass("Master password: ")
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
        if secrets.compare_digest(digest, stored):
            return Fernet(derive_key(password, salt))
        print("Incorrect password.")
    raise SystemExit("Too many failed attempts.")

def init_db():
    with sqlite3.connect(DB_FILE) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )""")

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in pwd) and any(c.isupper() for c in pwd)
                and any(c.isdigit() for c in pwd)
                and any(c in "!@#$%^&*()-_=+" for c in pwd)):
            return pwd

def add_credential(cipher):
    website = input("Website/App: ").strip()
    username = input("Username/Email: ").strip()
    password = getpass("Password (leave blank to generate): ")
    if not password:
        password = generate_password()
        print("Generated password:", password)
    encrypted = cipher.encrypt(password.encode()).decode()
    with sqlite3.connect(DB_FILE) as con:
        con.execute("INSERT INTO credentials(website, username, password) VALUES (?, ?, ?)",
                    (website, username, encrypted))
    print("Credential saved securely.")

def list_credentials(cipher, search=""):
    with sqlite3.connect(DB_FILE) as con:
        rows = con.execute("SELECT id, website, username, password FROM credentials "
                           "WHERE website LIKE ? OR username LIKE ? ORDER BY website",
                           (f"%{search}%", f"%{search}%")).fetchall()
    if not rows:
        print("No credentials found.")
        return
    for cid, website, username, encrypted in rows:
        try:
            password = cipher.decrypt(encrypted.encode()).decode()
        except InvalidToken:
            password = "[Unable to decrypt]"
        print(f"\nID: {cid}\nWebsite: {website}\nUsername: {username}\nPassword: {password}")

def update_credential(cipher):
    try:
        cid = int(input("Credential ID: "))
    except ValueError:
        print("Invalid ID."); return
    password = getpass("New password: ")
    if not password:
        password = generate_password()
        print("Generated password:", password)
    encrypted = cipher.encrypt(password.encode()).decode()
    with sqlite3.connect(DB_FILE) as con:
        cur = con.execute("UPDATE credentials SET password=? WHERE id=?", (encrypted, cid))
    print("Updated." if cur.rowcount else "ID not found.")

def delete_credential():
    try:
        cid = int(input("Credential ID: "))
    except ValueError:
        print("Invalid ID."); return
    with sqlite3.connect(DB_FILE) as con:
        cur = con.execute("DELETE FROM credentials WHERE id=?", (cid,))
    print("Deleted." if cur.rowcount else "ID not found.")

def main():
    print("\n=== PASSWORD MANAGER ===")
    setup_master()
    init_db()
    cipher = authenticate()
    while True:
        print("\n1. Add credential\n2. View all\n3. Search\n4. Update password\n5. Delete\n6. Generate password\n7. Exit")
        choice = input("Choose: ").strip()
        if choice == "1": add_credential(cipher)
        elif choice == "2": list_credentials(cipher)
        elif choice == "3": list_credentials(cipher, input("Search: ").strip())
        elif choice == "4": update_credential(cipher)
        elif choice == "5": delete_credential()
        elif choice == "6": print("Generated:", generate_password())
        elif choice == "7": print("Goodbye!"); break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()
