import hashlib
import pickle
import os

password = hashlib.new("sha256", b"toor")
username = "root"

user_pass = {
        username: password.digest(),
        }

with open(".usr_psw", "wb") as file:
    pickle.dump(user_pass, file)

print("dictionary has been written to the file")

with open(".usr_psw", "rb") as file:
    new_user_dict = pickle.load(file)

print(new_user_dict)
