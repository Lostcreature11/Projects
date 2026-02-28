

import os
import json
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

VAULT_FILE = "vault.json"


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(key, data):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, json.dumps(data).encode(), None)
    return base64.b64encode(nonce + encrypted).decode()


def decrypt_data(key, encrypted_text):
    raw = base64.b64decode(encrypted_text)
    nonce = raw[:12]
    ciphertext = raw[12:]
    aes = AESGCM(key)
    decrypted = aes.decrypt(nonce, ciphertext, None)
    return json.loads(decrypted.decode())


def load_vault():
    if not os.path.exists(VAULT_FILE):
        return None
    with open(VAULT_FILE, "r") as f:
        return json.load(f)


def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f)




def initialize_vault(master_password):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    vault = {
        "salt": base64.b64encode(salt).decode(),
        "data": {}
    }
    save_vault(vault)
    return key, vault


def unlock_vault(master_password):
    vault = load_vault()
    if vault is None:
        print("No vault found. Creating new vault...")
        return initialize_vault(master_password)

    salt = base64.b64decode(vault["salt"])
    key = derive_key(master_password, salt)
    return key, vault


def add_entry(key, vault):
    site = input("Website: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    encrypted = encrypt_data(key, {
        "username": username,
        "password": password
    })

    vault["data"][site] = encrypted
    save_vault(vault)
    print("Entry saved successfully.")


def view_entry(key, vault):
    site = input("Enter website to view: ").strip()

    if site not in vault["data"]:
        print("No entry found for this site.")
        return

    decrypted = decrypt_data(key, vault["data"][site])
    print("\n--- Stored Credentials ---")
    print("Username:", decrypted["username"])
    print("Password:", decrypted["password"])


def list_sites(vault):
    if not vault["data"]:
        print("Vault is empty.")
        return

    print("\nStored Websites:")
    for site in vault["data"]:
        print("-", site)




def main():
    print("==== Secure Password Manager ====\n")

    master_password = getpass.getpass("Enter Master Password: ")
    key, vault = unlock_vault(master_password)

    while True:
        print("\nChoose an option:")
        print("1. Add new entry")
        print("2. View entry")
        print("3. List all websites")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            add_entry(key, vault)

        elif choice == "2":
            view_entry(key, vault)

        elif choice == "3":
            list_sites(vault)

        elif choice == "4":
            print("Exiting Password Manager.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()