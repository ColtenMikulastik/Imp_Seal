
""" This program creates a user environemnt to encrypt and decrypt files """

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import base64
import binascii
import getpass
import hashlib
import os
import pickle
import secrets


# problems:
#   -if you run Imp from outside the folder, you will create a .usr_psw file outside of the dir
#   -password change functionality
#   -if you make a second account with same username, no errors, needs to be fixed
#       -idea for solving: add specific folder for users,
#           -then allow root to access all folders
#   -what if something is changed after encryption? this is important to fix


# constants
ENCODING = "utf-8"
HASH_ALGO = "sha256"


def csv_out(user_and_password_data_base):
    """outputs user, password, and salt into a csv file"""

    # where does user want to put information, and create the file
    csv_file_name = input("what filename would you like the csv file to be?:")
    os.system("touch " + csv_file_name)

    # write the data to file, using hex encoding, and then turning the hex into ascii
    with open(csv_file_name, mode='w', encoding="utf-8") as csv_file:
        for user, hash_n_salt in user_and_password_data_base.items():
            csv_file.write(user + "," + binascii.b2a_hex(hash_n_salt[0]).decode("ascii"))
            csv_file.write("," + binascii.b2a_hex(hash_n_salt[1]).decode("ascii") + "\n")


def decrypt_files(fern_key):
    """ uses fern_key argument to decrypt files in decrypt_me folder """
    # move to the decrypt file
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, "decrypt_me"))

    # find all the files inside
    files_to_decrypt = os.listdir()

    # loop through those files
    for file_name in files_to_decrypt:
        # take the encrypted data out
        with open(file_name, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        # decrypt the data
        decrypted_data = fern_key.decrypt(encrypted_data)
        # need to fix the file extension
        fix_ext = file_name.split('.')
        fix_ext.pop()
        fix_ext = '.'.join(fix_ext)
        # write to the files
        with open(fix_ext, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
        # notify the user
        print(fix_ext + " file done decrypting")
    # notify the user
    print("finished decrypting")


def encrypt_files(fern_key):
    """ uses fern_key argument to encrypt files in encrypt_me folder """
    # move to the encrypt_me directory
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, "encrypt_me"))

    # find all the files inside
    files_to_encrypt = os.listdir()

    #loop through the files
    for file_name in files_to_encrypt:
        # take the data
        with open(file_name, "rb") as decrypted_file:
            file_data = decrypted_file.read()
        # encrypt the data
        encrypted_data = fern_key.encrypt(file_data)
        # write encrypted data back into a .cy file
        with open(file_name + ".cy", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        print(file_name + " encryption complete")
    # notify the use job done
    print("all files in encrypt_me are now encrypted")
    os.chdir("..")


def post_auth_loop(password, salt):
    """ after authenticating the user can then use their password
    and salt to create a fernkey to encrypt and decrypt files"""

    # create the key from the clear text password
    key = derive_key(password, salt)
    loop_through = True
    print("Welcome!")
    while loop_through:
        print("--------------")
        # get encrypt or decry
        in_bool = None
        in_bool = input("would you like to (e)ncrypt, (d)ecrypt or (q)uit?:")

        if in_bool == 'e':
            # encrypt the file
            fern_key = Fernet(key)
            # send to function
            encrypt_files(fern_key)
        elif in_bool == 'd':
            # decrypt the file
            fern_key = Fernet(key)
            # send to function
            decrypt_files(fern_key)
        elif in_bool == 'q':
            loop_through = False
        else:
            print("could not understand input")


def generate_salt():
    return secrets.token_bytes(16)


def derive_key(password, salt):
    # options here should be looked up if confusing
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    derived_key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(derived_key)



def make_new_user(password_file, user_password):
    """ Creates a new user in the password file """
    os.system("clear")
    loop_make_user = True
    while loop_make_user:
        print("------------<>-----------")
        print("creating new user...")
        # I'm gonna store usernames as clear text
        username = input("username:")
        # I need to hash these
        password = getpass.getpass("password:")
        # using utf-8 byte encoding
        byte_password = bytes(password, ENCODING)
        # hashify
        pass_hash = hashlib.new(HASH_ALGO, byte_password)
        # retry the password to make sure that it's the same
        re_password = getpass.getpass("re-password:")
        byte_re_password = bytes(re_password, ENCODING)
        re_pass_hash = hashlib.new(HASH_ALGO, byte_re_password)

        print("------------<>-----------")

        if pass_hash.digest() == re_pass_hash.digest():
            print("storing username and password...")
            # creating a special salt for new user
            salt = generate_salt()
            user_hash_n_salt = [pass_hash.digest(), salt]
            # we need to add logic for same username
            user_password[username] = user_hash_n_salt
            # now we should write this to a file
            with open(password_file, "wb") as file:
                pickle.dump(user_password, file)
            loop_make_user = False
        else:
            print("Sorry, either these passwords do not match, or the resultant hashes are wrong.")
            print("please try again")
            # loop again


def remove_user(pass_file_name):
    """ Removes user from data base """
    # get username
    which_user = input("what user would you like to delete?:")
    # load in dictionary
    user_dict = {}
    with open(pass_file_name, "rb") as file:
        user_dict = pickle.load(file)
    #get password
    in_pass = getpass.getpass("what is this user's password?:")
    in_encoded_pass = bytes(in_pass, ENCODING)
    hash_pass = hashlib.new(HASH_ALGO, in_encoded_pass)
    #look for user
    found_user = False
    for dict_user, hash_n_salt in user_dict.items():
        if dict_user == which_user and hash_pass.digest() == hash_n_salt[0]:
            found_user = True
        else:
            pass
    if found_user:
        # remove user from the dictionary
        del user_dict[which_user]
        print("This username was found and is now deleted")
        # now I am going to reload the dictionary into the file
        with open(pass_file_name, "wb") as file:
            pickle.dump(user_dict, file)
    else:
        print("This username was not found and can't be deleted")


def login(user_pass_data_base):
    """check to see if user is in data base"""
    # at some point, I want to add unencoding files so
    # that the program has a purpose
    # get username and password
    in_user = input("username:")
    in_pass = getpass.getpass("password:")
    print("logging in...")
    encod_in_pass = bytes(in_pass, ENCODING)
    hash_in_pass = hashlib.new(HASH_ALGO, encod_in_pass)
    # save the salt
    salt = b''
    # look for information in dictionary
    found_user = False
    for dict_user, hash_n_salt in user_pass_data_base.items():
        if dict_user == in_user and hash_in_pass.digest() == hash_n_salt[0]:
            found_user = True
            salt = hash_n_salt[1]
        else:
            pass
    if found_user:
        print("logged in!")
        # might want to send my encoded password.... ?
        post_auth_loop(in_pass, salt)
    else:
        print("authentication failed...")


def make_password_file(password_file_name):
    # touching file to store passwords
    # if it exists, there should be no problem
    # also making the file hidden :^)
    os.system("touch " + password_file_name)


def main():
    """ unloads password database, and loops initial interface """
    # this is the password files
    password_file_name = ".usr_psw"
    make_password_file(password_file_name)
    os.system("clear")

    # this is where I will create the dictionary
    user_and_password_data_base = {}
    with open(password_file_name, "rb") as file:
        user_and_password_data_base = pickle.load(file)

    print("Imp_Seal ver 1")
    loop_prompt = True
    # create a ui
    while loop_prompt:
        print("------------<>-----------")
        print("please choose an option below:")
        print("------------<>-----------")
        print("c - create new user")
        print("r - remove user")
        print("l - login")
        print("b - clear screen")
        print("q - quit")
        print("o - csv output")
        print("------------<>-----------")
        log_prompt = input(": ")
        if log_prompt == 'c':
            make_new_user(password_file_name, user_and_password_data_base)
        elif log_prompt == 'l':
            login(user_and_password_data_base)
        elif log_prompt == 'r':
            remove_user(password_file_name)
        elif log_prompt == 'b':
            os.system("clear")
        elif log_prompt == 'o':
            csv_out(user_and_password_data_base)
        elif log_prompt == 'q':
            print("you wish to quit")
            loop_prompt = False
        else:
            print("lets try that again... (hint: lower-case)")

if __name__ == "__main__":
    main()
