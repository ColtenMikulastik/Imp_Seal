import cryptography
from cryptography.fernet import Fernet

# creates your key for encrytion
def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)


# load the created encrytion key
def load_key():
    return open("key.key", "rb").read()

def encrypt(file_name, key):
    # encrypt file
    f = Fernet(key)
    with open(file_name, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)


def decrypt(file_name, key):
    #decrypt a file
    f = Fernet(key)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_name, "wb") as file:
        file.write(decrypted_data)


key = load_key()
file_name = "test.txt"
decrypt(file_name, key)
