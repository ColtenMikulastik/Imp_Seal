import hashlib
import pickle
import os

password = hashlib.new("sha256", b"password")
username = "pickle"
password_two = hashlib.new("sha256", b"new_password")
username_two = "usa"
password_three = hashlib.new("sha256", b"new_password")
username_three = "agreerere"



user_pass = {
        username: password.digest(),
        username_two: password_two.digest(),
        username_three: password_three.digest()
        }

with open(".usr_psw", "wb") as file:
    pickle.dump(user_pass, file)

print("dictionary has been written to the file")

with open(".usr_psw", "rb") as file:
    new_user_dict = pickle.load(file)

print(new_user_dict)
