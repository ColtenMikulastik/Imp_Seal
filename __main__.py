import hashlib
import os
import pickle

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
        byte_password = bytes(password,"utf-8")
        # hashify
        pass_hash = hashlib.new("sha256", byte_password)
        # retry the password to make sure that it's the same
        re_password = input("re-password:")
        byte_re_password = bytes(re_password,"utf-8")
        re_pass_hash = hashlib.new("sha256", byte_re_password)
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
        print("c - create new user")
        print("l - login")
        print("q - quit")
        print("------------<>-----------")
        log_prompt = input(": ")
        if log_prompt == 'c':
            make_new_user(password_file, user_password)
            os.system("clear")
        elif log_prompt == 'l':
            print("you pressed l")
        elif log_prompt == 'q':
            print("you wish to quit")
            loop_over = False
        else:
            print("lets try that again... (hint: lower-case)")

if __name__ == "__main__":
    main()
