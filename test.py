

import math

def bad_search():
    for place in range(len(place_list) - 1, -1, -1):
        for letter in range(0, len(omni_list)):
            place_list[place] = letter
            print(omni_list[place_list[0]] + omni_list[place_list[1]] + omni_list[place_list[2]])



pass_len = 3

alpha_list = ["a", "b", "c" ] 

omni_list = alpha_list

# create the list wherethe password will go
place_list = [0] * pass_len

allpp = len(omni_list) ** pass_len
print(allpp)
print(allpp / len(omni_list)) 

iterator = int(0)
all_pass_found = False

while all_pass_found != True:

    jiterator = int(len(place_list) - 1)
    print(place_list)
    while jiterator >= 0:
        if place_list[jiterator] >= len(omni_list):
            place_list[jiterator - 1] = place_list[jiterator - 1] + 1
            place_list[jiterator] = 0
        jiterator = jiterator - 1

    print(omni_list[place_list[0]] + omni_list[place_list[1]] + omni_list[place_list[2]])
    place_list[-1] = place_list[-1] + 1
    iterator = iterator + 1
 
    # if all possible passwords are found then we quit
    if iterator >= allpp:
        all_pass_found = True
        



