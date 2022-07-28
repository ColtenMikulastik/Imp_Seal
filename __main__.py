import hashlib
import os


def main():
    os.system("clear")
    print("Imp_Seal ver 1")
    loop_over = True
    while loop_over:
        print("------------<>-----------")
        print("c - create new user")
        print("l - login")
        print("q - quit")
        print("------------<>-----------")
        log_prompt = input(": ")
        if log_prompt == 'c':
            print("you pressed c")
        elif log_prompt == 'l':
            print("you pressed l")
        elif log_prompt == 'q':
            print("you wish to quit")
            loop_over = False
        else:
            print("lets try that again...")

if __name__ == "__main__":
    main()
