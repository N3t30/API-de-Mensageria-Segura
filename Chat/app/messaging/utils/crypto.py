import os

from cryptography.fernet import Fernet

key = os.getenv("MESSAGE_ENCRYPTION_KEY").encode()
fernet = Fernet(key)


def encrypt_message(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()


def decrypt_message(text: str) -> str:
    return fernet.decrypt(text.encode()).decode()
