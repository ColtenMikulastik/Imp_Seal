
# variables that define the scan
pass_len = 4
alpha_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
num_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
omni_list = alpha_list + num_list

# create the list wherethe password will go
place_list = [0] * pass_len
allpp = len(omni_list) ** pass_len

# print information about the list generations
print(str(allpp) + "possible passwords")

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

