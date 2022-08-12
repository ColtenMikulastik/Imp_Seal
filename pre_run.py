import hashlib
import pickle
import os

# encryption libs

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets
import base64
import getpass


def generate_salt():
    return secrets.token_bytes(16)


def derive_key(salt, password):
    # options here should be looked up if confusing
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


password = hashlib.new("sha256", b"toor")
username = "root"

# part of the new functionality
# add salt
salt = generate_salt()

user_pass = {
        username: [password.digest(), salt]
        }

with open(".usr_psw", "wb") as file:
    pickle.dump(user_pass, file)

print("dictionary has been written to the file")

with open(".usr_psw", "rb") as file:
    new_user_dict = pickle.load(file)

print(new_user_dict)
