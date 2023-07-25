# Colten (Luca) Vance Mikulastik

""" This program is created to break hashes through brute force
utilizing the csv file from before, this program will attempt to 
break the hashes and print a found password when completed. """



def show_target_info(target_info):
    for feild, value in target_info.items():
        print(feild + ":" + value)


def brute_force_hash_break(target_info):
    """ uses a brute force method to break the given account's hash """
    print("you are running the brute force hash break...")


def choose_target(target_info):
    """ Uses directory structure to find a file to search for the csv file, and returns that target"""
    print("you are now choosing target...")
    target_file = input("csv file name in the local directory:")
    target_info["file"] = target_file

    target_user = input("User name in the csv file:")
    target_info["user"] = target_user

    return target_info


def main():
    print("Welcome to \"hash_breaker\"")
    print("=============================")

    # defines the target information
    target_info = {"file": "output.csv", "user": "root"}
    loop_prompt = True

    while loop_prompt:
    
        print("please choose an option below:")
        print("=============================")
        print("c - choose target in csv file")
        print("p - print choosen target")
        print("r - run attack")
        print("q - quit")
        print("=============================")
        option = input("option:")

        if option == 'c':
            target_info = choose_target(target_info)
        elif option == 'p':
            show_target_info(target_info)
        elif option == 'r':
            brute_force_hash_break(target_info)
        elif option == 'q':
            loop_prompt = False
        else:
            print("that is not one of the options (hint: try lowercase)")



if __name__ == "__main__":
    main()
