import os
from cryptography.fernet import Fernet

if not os.path.exists("config.json"):
    raise FileNotFoundError("config.json not found")

if os.path.exists("key.key"):
    with open("key.key", "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()

fernet = Fernet(key)

with open("key.key", "wb") as key_file:
    key_file.write(key)

with open("config.json", "rb") as config_file:
    encrypted_config = fernet.encrypt(config_file.read())
    with open("config.encrypted", "wb") as config_file:
        config_file.write(encrypted_config)
