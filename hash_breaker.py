# Colten (Luca) Vance Mikulastik

""" This program is created to break hashes through brute force
utilizing the csv file from before, this program will attempt to 
break the hashes and print a found password when completed. """



def brute_force_hash_break(target):
    """ uses a brute force method to break the given account's hash """
    print("you are running the brute force hash break...")

def choose_target(target):
    """ Uses directory structure to find a file to search for the csv file, and returns that target"""
    print("you are now choosing target...")

    return target



def main():
    print("Welcome to \"hash_breaker\"")
    print("=============================")
   
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

        # defines the target file for attack, default is output.csv
        target = "output.csv"

        if option == 'c':
            target = choose_target(target)
        elif option == 'p':
            print(target)
        elif option == 'r':
            brute_force_hash_break(target)
        elif option == 'q':
            loop_prompt = False
        else:
            print("that is not one of the options (hint: try lowercase)")



if __name__ == "__main__":
    main()
