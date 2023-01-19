# this is a working test run example for pos_loop.py

n=5 #50 
th_init=4
heal_speed=0 
hf_dmg=1
location = [(0,1),(1,0),(4,4),(1,2)] # put a 0 if location is not given
location2= [(0,2),(1,2),(4,3),(1,2)] # put a 0 if location2 is not provided 
frac = 0.6
i_value = 0
zs_big = 0 # put 0 if you don't want to add a zs_big 
ths_big = 0 # put 0 if you don't want to add a ths_big 
seed_val = 42 

zs_timeseries, ths_timeseries = pos_loop (n, th_init, hf_dmg, frac, location, location2, heal_speed, i_value = 0, zs_big = 0, ths_big = 0, seed_val=42)

print(zs_timeseries)
print(ths_timeseries)
