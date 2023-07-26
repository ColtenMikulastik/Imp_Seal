

import math

pass_len = 3

alpha_list = ["a", "b", "c" ] 

omni_list = alpha_list

# create the list wherethe password will go
place_list = [len(alpha_list) - 1] * pass_len

allpp = len(omni_list) ** pass_len
print(allpp)
print(allpp / len(omni_list))

# for delta in range(0, (len(omni_list) ** pass_len)):
    
for place in range(len(place_list) - 1, -1, -1):
    for letter in range(0, len(omni_list)):
        place_list[place] = letter
        print(omni_list[place_list[0]] + omni_list[place_list[1]] + omni_list[place_list[2]])


            
        



