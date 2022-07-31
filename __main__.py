import hashlib
import os
import pickle

# problems:
#   -if you run Imp from outside the folder, you will create a .usr_psw file outside of the dir
#   -if you make a second account with same username, no errors, needs to be fixed
#   -no login yet

# constants
ENCODING = "utf-8"
HASH_ALGO = "sha256"


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
        password = input("password:")
        # using utf-8 byte encoding
        byte_password = bytes(password, ENCODING)
        # hashify
        pass_hash = hashlib.new(HASH_ALGO, byte_password)
        # retry the password to make sure that it's the same
        re_password = input("re-password:")
        byte_re_password = bytes(re_password, ENCODING)
        re_pass_hash = hashlib.new(HASH_ALGO, byte_re_password)

        print("------------<>-----------")
    
        if(pass_hash.digest() == re_pass_hash.digest()):
            print("storing username and password...")
            # we need to add logic for same username
            user_password[username] = pass_hash.digest()
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
    in_pass = input("what is this user's password?:")
    in_encoded_pass = bytes(in_pass, ENCODING)
    hash_pass = hashlib.new(HASH_ALGO, in_encoded_pass)
    #look for user
    found_user = False
    for dict_user, dict_pass in user_dict.items():
        if dict_user == which_user and hash_pass.digest() == dict_pass:
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
    in_pass = input("password:")
    print("logging in...")
    encod_in_pass = bytes(in_pass, ENCODING)
    hash_in_pass = hashlib.new(HASH_ALGO, encod_in_pass)
    # look for information in dictionary
    found_user = False
    for dict_user, dict_pass in user_pass_dict.items():
        if dict_user == in_user and hash_in_pass.digest() == dict_pass:
            found_user = True
        else:
            pass
    if found_user:
        print("logged in!")
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
