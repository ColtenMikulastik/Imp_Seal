# Colten (Luca) Vance Mikulastik

""" This program is created to break hashes through brute force
utilizing the csv file from before, this program will attempt to 
break the hashes and print a found password when completed. """


import binascii
import hashlib
import time

# global list varibles
ALPHA_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

NUM_LIST = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def time_diff(past_time, now_time):
    """ takes two strftime strings and returns the difference between the two """
    past_time = past_time.split(':')
    now_time = now_time.split(':')
    diff_time = list()

    for i in range(0, len(past_time)):
        diff_time.append(str(int(now_time[i]) - int(past_time[i])))
    
    return diff_time


def load_target_hash(target_info):
    """ loads the information defined in the csv file """
    # read lines from the csv file
    with open(target_info["file"], mode='r', encoding="utf-8") as csv_file:
        print("\tfile found...")
        lines = csv_file.readlines()

    for line in lines:
        csv_list = line.split(',')
        if csv_list[0] == target_info["user"]:
            print("\tuser found...")
            target_info["hash"] = csv_list[1]
            # remove the new line character
            target_info["salt"]  = csv_list[2][:-1]

    # call function to print info
    show_target_info(target_info)


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
    # add global varibles to character list
    omni_list = ALPHA_LIST + NUM_LIST

    # create the list where num to character mapping goes
    place_list = [0] * int(target_info["pass_len"])

    # all possible passwords created: characters ^ (password_length)
    allpp = len(omni_list) ** int(target_info["pass_len"])

    # print information about the list generations
    print("\n\t=============================")
    print("\tthere are " + str(allpp) + " possible passwords...")
    last_call = input("\tdo you want to start the attack?(y/n)")
    if last_call != 'y':
        print("\tokay returning to main menue...")
        return

    # get the current time in format year:month:day:hours:min:sec
    before_attack_time = time.strftime("%Y:%m:%d:%H:%M:%S", time.localtime())
    print(before_attack_time)

    # set some varibles for the loop
    iterator = int(0)
    all_pass_found = False

    # this loop generate all possible passwords
    while all_pass_found is False:
        # round before applying to omni_list to avoid going out of bounds
        rounder = int(len(place_list) - 1)
        while rounder >= 0:
            if place_list[rounder] >= len(omni_list):
                place_list[rounder - 1] = place_list[rounder - 1] + 1
                place_list[rounder] = 0
            rounder = rounder - 1

        # creating the password variable
        pass_attempt = []

        # load information into the password attempt
        for letter in place_list:
            pass_attempt.append(omni_list[letter])

        # join the characters and print the output
        pass_attempt = ''.join(pass_attempt)
        print("attempting password: " + pass_attempt)

        # hashify this biz
        pass_attempt_bytes = bytes(pass_attempt, target_info["encoding"])
        pass_attempt_hash = hashlib.new(target_info["hash_algo"], pass_attempt_bytes)

        # printing the hash
        real_pass_attempt_hash = binascii.b2a_hex(pass_attempt_hash.digest()).decode("ascii")

        if real_pass_attempt_hash == target_info["hash"]:
            print("password found!")
            # calculate the difference in time
            after_attack_time = time.strftime("%Y:%m:%d:%H:%M:%S", time.localtime())
            print(after_attack_time)
            print("attack took: ", end='')
            diff_time = time_diff(before_attack_time, after_attack_time)
            print(diff_time)
            print("password hash: " + real_pass_attempt_hash)
            print("password     : " + pass_attempt)
            target_info["password"] = pass_attempt
            input("press enter to continue:")
            return

        # subtract one from the last place
        place_list[-1] = place_list[-1] + 1
        iterator = iterator + 1

        # if all possible passwords are found then we quit
        if iterator >= allpp:
            all_pass_found = True

    print("\n\t=============================")
    print("\tall passwords checked returning to the main menue")


def choose_target(target_info):
    """ Uses directory structure to find a file to search for the csv file,
    and returns that target"""

    print("\n\t=============================")
    print("\tyou are now choosing target:")
    print("\t=============================")

    # allows user to input target info
    target_file = input("\tcsv file name in the local directory:")
    target_info["file"] = target_file

    target_user = input("\tuser name in the csv file:")
    target_info["user"] = target_user


def main():
    """ Runs the interactive prompt for the user """
    print("Welcome to \"hash_breaker\"")
    print("=============================")

    # defines the target information
    target_info = {"file": "output.csv",
                   "user": "root",
                   "hash": "!unknown!",
                   "salt": "!unknown!",
                   "encoding": "utf-8",
                   "hash_algo": "sha256",
                   "pass_len": "4",
                   "password": "!unknown!"}

    # sets looping to true
    loop_prompt = True

    # loops until user presses q, allowing for other options
    while loop_prompt:
        print("please choose an option below:")
        print("=============================")
        print("c - choose target in csv file")
        print("l - load info from csv")
        print("p - print choosen target")
        print("r - run attack")
        print("q - quit")
        print("=============================")
        option = input("option:")

        # the decission tree
        if option == 'c':
            choose_target(target_info)
        elif option == 'l':
            load_target_hash(target_info)
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
