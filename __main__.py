import hashlib
import os
import pickle

# encryption libs

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import secrets
import base64
import getpass


# problems:
#   -add file encrypotion
#       -create the encryption key from the un-hashed password
#       -give option to encrypt or unencrypt eveything in specific file after user is authenticated
#   -if you run Imp from outside the folder, you will create a .usr_psw file outside of the dir
#   -if you make a second account with same username, no errors, needs to be fixed

# constants
ENCODING = "utf-8"
HASH_ALGO = "sha256"


def decrypt_files(fern_key):
    # move to the decrypt file
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, "decrypt_me"))
    
    # find all the files inside
    files_to_decrypt = os.listdir()

    # loop through those files
    for file_name in files_to_decrypt:
        # take the encrypted data out
        with open(file_name, "rb") as f:
            encrypted_data = f.read()
        # decrypt the data
        decrypted_data = fern_key.decrypt(encrypted_data)
        # need to fix the file extension
        fix_ext = file_name.split('.')
        fix_ext.pop()
        fix_ext = '.'.join(fix_ext)
        # write to the files
        with open(fix_ext, "wb") as f:
            f.write(decrypted_data)
        # notify the user
        print(fix_ext + " file done decrypting")
    # notify the user
    print("finished decrypting")
    


def encrypt_files(fern_key):
    # move to the encrypt_me directory
    cur_dir = os.getcwd()
    os.chdir(os.path.join(cur_dir, "encrypt_me"))
    
    # find all the files inside
    files_to_encrypt = os.listdir()
    
    #loop through the files
    for file_name in files_to_encrypt: 
        # take the data
        with open(file_name, "rb") as f:
            file_data = f.read()
        # encrypt the data
        encrypted_data = fern_key.encrypt(file_data)
        # write encrypted data back into a .cy file
        with open(file_name + ".cy", "wb") as f:
            f.write(encrypted_data)
        print(file_name + " encryption complete")
    # notify the use job done
    print("all files in encrypt_me are now encrypted")
    os.chdir("..")

def post_auth_loop(password, salt):
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
    '''Creates a new user in the password file'''
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
    
        if(pass_hash.digest() == re_pass_hash.digest()):
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
            return
        else:
            print("Sorry, either these passwords do not match, or the resultant hashes are wrong.")
            print("please try again")
            # loop again


def remove_user(pass_file_name, user_password):
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
        return
    else:
        print("This username was not found and can't be deleted")
        return
  

def login(pass_file_name, user_pass_dict):
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
    for dict_user, hash_n_salt in user_pass_dict.items():
        if dict_user == in_user and hash_in_pass.digest() == hash_n_salt[0]:
            found_user = True
            salt = hash_n_salt[1]
        else:
            pass
    if found_user:
        print("logged in!")
        # might want to send my encoded password.... ?
        post_auth_loop(in_pass, salt)
        return
    else:
        print("authentication failed...")
        return
 

def make_password_file(pass_file_name):
    # touching file to store passwords
    # if it exists, there should be no problem
    # also making the file hidden :^)
    os.system("touch " + pass_file_name)


def main():
    # this is the password files
    password_file = ".usr_psw"
    make_password_file(password_file)
    os.system("clear")

    # this is where I will create the dictionary
    user_password = {}
    with open(password_file, "rb") as file:
        user_password = pickle.load(file)

    print("Imp_Seal ver 1")
    loop_over = True
    # create a ui
    while loop_over:
        print("------------<>-----------")
        print("please choose an option below:")
        print("------------<>-----------")
        print("c - create new user")
        print("r - remove user")
        print("l - login")
        print("b - clear screen")
        print("q - quit")
        print("------------<>-----------")
        log_prompt = input(": ")
        if log_prompt == 'c':
            make_new_user(password_file, user_password)
        elif log_prompt == 'l':
            login(password_file, user_password)
        elif log_prompt == 'r':
            remove_user(password_file, user_password)
        elif log_prompt == 'b':
            os.system("clear")
        elif log_prompt == 'q':
            print("you wish to quit")
            loop_over = False
        else:
            print("lets try that again... (hint: lower-case)")

if __name__ == "__main__":
    main()
