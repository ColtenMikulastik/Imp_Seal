# Colten (Luca) Vance Mikulastik

""" This program is created to break hashes through brute force
utilizing the csv file from before, this program will attempt to 
break the hashes and print a found password when completed. """


import binascii
import hashlib

import time

class Target:
    def __init__(self, csv_file = "output.csv", user = "root", encoding = "utf-8", hash_algo = "sha256", pass_len = 4):
        """ create target """
        self.csv_file = csv_file
        self.user = user
        self.encoding = encoding
        self.hash_algo = hash_algo
        self.pass_len = pass_len
        self.found_hash = False
        self.found_password = False

    def print_info(self):
        """ print infomration about the target """
        # print the known target information
        print("\n\t=============================")
        print("\tprinting target info:")
        print("\t=============================")
        print("\tcsv file:        " + self.csv_file)
        print("\tusername:        " + self.user)
        print("\tencoding:        " + self.encoding)
        print("\thashing algo:    " + self.hash_algo)
        print("\tpassword length: " + str(self.pass_len))

        # if hash has been found show user
        if self.found_hash:
            print("\thash:            " + self.hash)
            print("\tsalt:            " + self.salt)
        else:
            print("\thash not found... (load csv file first)")

        # if password has been found show user
        if self.found_password:
            print("\tpassword         " + self.password)
        else:
            print("\tpassword not found... (run attack to get password)")

    def load_csv_file(self):
        """ calling this function loads information from the csv file given """
        with open(self.csv_file, mode='r', encoding="utf-8") as csv_file:
            print("\tfile found...")
            lines = csv_file.readlines()

        for line in lines:
            csv_list = line.split(',')
            if csv_list[0] == self.user:
                print("\tuser found...")
                self.hash = csv_list[1]
                # remove newline char
                self.salt = csv_list[2][:-1]

        self.found_hash = True
        self.print_info()

# global list varibles
ALPHA_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

NUM_LIST = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def time_diff(past_time, now_time):
    """ takes two floats and returns the difference between the two in a list """
    # calc difference in time create variables
    diff_time = now_time - past_time

    diff_time_list = list()

    # append and remove hours
    diff_time_list.append(str(int(diff_time / 3600)))
    diff_time = diff_time % 3600

    # append and remove min
    diff_time_list.append(str(int(diff_time / 60)))
    diff_time = diff_time % 60

    # append seconds
    diff_time_list.append(str(int(diff_time)))

    return diff_time_list


def brute_force_hash_break(target):
    """ uses a brute force method to break the given account's hash """
    print("\n\t=============================")
    print("\trunning attack on target:")
    print("\t=============================")
    # add global varibles to character list
    omni_list = ALPHA_LIST + NUM_LIST

    # create the list where num to character mapping goes
    place_list = [0] * int(target.pass_len)

    # all possible passwords created: characters ^ (password_length)
    allpp = len(omni_list) ** int(target.pass_len)

    # print information about the list generations
    print("\n\t=============================")
    print("\tthere are " + str(allpp) + " possible passwords...")
    last_call = input("\tdo you want to start the attack?(y/n)")
    if last_call != 'y':
        print("\tokay returning to main menue...")
        return

    # save time in seconds
    before_attack_time = time.time()

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
        pass_attempt_bytes = bytes(pass_attempt, target.encoding)
        pass_attempt_hash = hashlib.new(target.hash_algo, pass_attempt_bytes)

        # printing the hash
        real_pass_attempt_hash = binascii.b2a_hex(pass_attempt_hash.digest()).decode("ascii")

        if real_pass_attempt_hash == target.hash:
            print("password found!")
            # calculate the difference in time
            after_attack_time = time.time()
            diff_time = time_diff(before_attack_time, after_attack_time)
            # only going to print the hours min and sec!!!
            print("attempt took:")
            print("hours: " + diff_time[0] + " min: " + diff_time[1] + " sec: " + diff_time[2])
            print("password hash: " + real_pass_attempt_hash)
            print("password     : " + pass_attempt)
            target.found_password = True
            target.password = pass_attempt
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
    after_attack_time = time.time()
    diff_time = time_diff(before_attack_time, after_attack_time)
    # only going to print the hours min and sec!!!
    print("\tattempt took:")
    print("\thours: " + diff_time[0] + " min: " + diff_time[1] + " sec: " + diff_time[2])


def choose_target(target):
    """ Uses directory structure to find a file to search for the csv file,
    and returns that target"""

    print("\n\t=============================")
    print("\tyou are now choosing target:")
    print("\t=============================")

    # allows user to input target info
    target.csv_file = input("\tcsv file name in the local directory:")
    target.user = input("\tuser name in the csv file:")


def main():
    """ Runs the interactive prompt for the user """
    print("Welcome to \"hash_breaker\"")
    print("=============================")

    # defines the target information
    target = Target()

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
            choose_target(target)
        elif option == 'l':
            target.load_csv_file()
        elif option == 'p':
            target.print_info()
        elif option == 'r':
            brute_force_hash_break(target)
        elif option == 'q':
            loop_prompt = False
        else:
            print("that is not one of the options (hint: try lowercase)")

        print("\n\n")



if __name__ == "__main__":
    main()
