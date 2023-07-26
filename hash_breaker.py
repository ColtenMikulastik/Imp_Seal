# Colten (Luca) Vance Mikulastik

""" This program is created to break hashes through brute force
utilizing the csv file from before, this program will attempt to 
break the hashes and print a found password when completed. """

def show_target_info(target_info):
    """ prints the dictionary for the  target information """
    print("\n\t=============================")
    print("\tprinting target info:")
    print("\t=============================")

    # loops through dictionary printing information about set target
    for feild, value in target_info.items():
        print("\t" + feild + ":" + value)


def brute_force_hash_break(target_info):
    """ uses a brute force method to break the given account's hash """
    print("\n\t=============================")
    print("\trunning attack on target:")
    print("\t=============================")

    # read lines from the csv file
    with open(target_info["file"], mode='r', encoding="utf-8") as csv_file:
        print("\tfile found...")
        lines = csv_file.readlines()
    
    # prepare storage for the hash and salt
    target_hash = ""
    target_salt = ""

    for line in lines:
        csv_list = line.split(',')
        if csv_list[0] == target_info["user"]:
            print("\tuser found...")
            target_hash = csv_list[1]
            # remove the new line character
            target_salt = csv_list[2][:-1]

    # print out the target info
    print("\n\t=============================")
    print("\ttarget: " + target_info["user"])
    print("\thash:   " + target_hash)
    print("\tsalt:   " + target_salt)
    

    # for now we are just going to do numbers and letters, and only four characters
    # I will likely be adding this to the target info dictionary
    # variables that define the scan
    alpha_char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    num_char_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    pass_length = 4
    omni_list = alpha_char_list

    # create the list wherethe password will go
    place_list = [0] * pass_length
    allpp = len(omni_list) ** pass_length

    # print information about the list generations
    print("\n\t=============================")
    print("\tthere are " + str(allpp) + " possible passwords...")
    last_call = input("\tdo you want to start the attack?(y/n)")
    if(last_call != 'y'):
        print("\tokay returning to main menue...")
        return


    # set some varibles for the loop
    iterator = int(0)
    all_pass_found = False

    # this loop generate all possible passwords
    while all_pass_found != True:
        # round before applying to omni_list to avoid going out of bounds
        rounder = int(len(place_list) - 1)
        while rounder >= 0:
            if place_list[rounder] >= len(omni_list):
                place_list[rounder - 1] = place_list[rounder - 1] + 1
                place_list[rounder] = 0
            rounder = rounder - 1

        # print the output
        for letter in place_list:
            print(omni_list[letter], end="")
        print()

        # subtract one from the last place
        place_list[-1] = place_list[-1] + 1
        iterator = iterator + 1

        # if all possible passwords are found then we quit
        if iterator >= allpp:
            all_pass_found = True
    print("\n\t=============================")
    print("\tall passwords checked returning to the main menue")


def choose_target(target_info):
    """ Uses directory structure to find a file to search for the csv file, and returns that target"""
    print("\n\t=============================")
    print("\tyou are now choosing target:")
    print("\t=============================")

    # allows user to input target info
    target_file = input("\tcsv file name in the local directory:")
    target_info["file"] = target_file

    target_user = input("\tuser name in the csv file:")
    target_info["user"] = target_user

    return target_info


def main():
    """ Runs the interactive prompt for the user """
    print("Welcome to \"hash_breaker\"")
    print("=============================")

    # defines the target information
    target_info = {"file": "output.csv", "user": "root"}
    # sets looping to true
    loop_prompt = True

    # loops until user presses q, allowing for other options
    while loop_prompt:
        print("please choose an option below:")
        print("=============================")
        print("c - choose target in csv file")
        print("p - print choosen target")
        print("r - run attack")
        print("q - quit")
        print("=============================")
        option = input("option:")

        # the decission tree
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

        print("\n\n")



if __name__ == "__main__":
    main()
