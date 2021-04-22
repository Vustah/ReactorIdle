import sys
import math as m

num_solar = float(sys.argv[1])
Heat_produced = 15.2
Generator_heat_capacity = 11.4

num_generator_needed= (num_solar*Heat_produced)/Generator_heat_capacity
if num_generator_needed < 1:
    heat_ratio = Generator_heat_capacity/Heat_produced
    rounded_heat_ratio = round(heat_ratio*2)/2
    if rounded_heat_ratio > heat_ratio:
        rounded_heat_ratio = rounded_heat_ratio-0.5
    print("Number of solar cells per generator: ", rounded_heat_ratio)
else:
    rounded_gen_needed = round(num_generator_needed*2)/2
    if rounded_gen_needed < num_generator_needed:
        rounded_gen_needed = rounded_gen_needed+0.5
    print("number of generators per solar cell: ", (rounded_gen_needed))