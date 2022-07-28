import hashlib
import os

def make_new_user():
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
            # this is where I would store the passwords
            loop_make_user = False
            return
        else:
            print("Sorry, either these passwords do not match, or the resultant hashes are wrong.")
            print("please try again")
            # loop again
    

def main():
    os.system("clear")
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
            make_new_user()
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
