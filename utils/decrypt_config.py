import os
from cryptography.fernet import Fernet

if not os.path.exists("config.encrypted"):
    raise FileNotFoundError("config.encrypted not found")

if os.path.exists("key.key"):
    with open("key.key", "rb") as key_file:
        key = key_file.read()
else:
    key = os.environ.get("KEY", "").encode()

if not key:
    raise ValueError("No value of KEY has been provided")

fernet = Fernet(key)

with open("key.key", "wb") as key_file:
    key_file.write(key)

with open("config.encrypted", "rb") as config_file:
    encrypted_config = config_file.read()
    decrypted_config = fernet.decrypt(encrypted_config)

# print(decrypted_config)
with open("config.json", "wb") as config_file:
    config_file.write(decrypted_config)
