def meltponds_nonconserve(n,iters,th_init,heal_speed,hf_dmg,rng,location, location2, frac, i_value, zs_big, ths_big):
    # separate the location and location 2 statements to an if else statement 
    try:
        if location:
            pos_pond_loc = np.empty([2,iters]) # this is the maximums size that the possible location array can be 
            for loc in range(len(location)):
                pos_pond_loc[0][loc] = location[loc][0]
                pos_pond_loc[1][loc] = location[loc][1]
            print('location is given')
            pos_pond_loc = pos_pond_loc[:,:len(location)]
    # now there is an array of possible locations for the meltponds, it is 2 rows - top is row number and nottom is the column number 
    except: 
        pos_pond_loc = rng.integers(n,size=(2,iters),dtype = int) # this line is working, locations for the meltponds to be added at random 
        pos_pond_loc.astype(int)
        print('location is not given')
        
    try:
        if location2:
            pos_pond_loc2 = np.empty([2,iters])# for the heal speed array 
            for loc2 in range(len(location2)):
                pos_pond_loc2[0][loc2] = location2[loc2][0] # for the heal speed array 
                pos_pond_loc2[1][loc2] = location2[loc2][1]
            print('fracture healing location given')
            pos_pond_loc2 = pos_pond_loc2[:,:len(location2)]
    # now there is an array of possible locations for the meltponds, it is 2 rows - top is row number and nottom is the column number 
    except: 
        pos_pond_loc2 = rng.integers(n,size=(heal_speed,2,iters), dtype = int) #line for if heal speed is added to this function 
        pos_pond_loc2.astype(int)
        print('fracture healing location not given')
    # at this point if the user decided not to add a meltpond location array they automatically have a random integer array of seeds
    # but we need to cut down the size of pos_pond_loc to where just the values are
    

    #print(pos_pond_loc)
    #print(len(pos_pond_loc[0]))
    frac_pond = math.ceil(frac*len(pos_pond_loc[0]))
    #print(frac_pond)
    frac_healing = math.ceil(frac*len(pos_pond_loc2[0]))
    seeds = pos_pond_loc[:,:frac_pond] 
    seeds2 = pos_pond_loc2[:,:frac_healing]
    seeds = seeds.astype(int)
    seeds2 = seeds2.astype(int)
    
    #print(seeds)
    #print(seeds2)
    
    try:
        if len(zs_big) > 0:
            z = zs_big
            th = ths_big
    except:
        z = np.zeros((n,n),dtype=int) #,dtype=float, zeros was empty 
        th=th_init*np.ones((n,n),dtype = int)

    # for this first round of edits all the meltponds will gain water, but in the future this should be separate, so have a running 
    # number starting at 0 as the iteration for this for loop adds a pond depth, only adding 1 unit to a pond at each start of the advection cycle 
    
    #print(z)
    
    i = i_value
    z[seeds[0][i],seeds[1][i]] += 1 
    z = z.astype(int)
    
    #print(i)
    
    for q in range(heal_speed):
        if (z[seeds2[q][0][i]],[seeds2[q][1][i]] == 0):
            th[seeds2[q][0][i],seeds2[q][1][i]]=th[seeds2[q][0][i],seeds2[q][1][i]] + 1
            th[seeds2[q][0][i],seeds2[q][1][i]]=min(pd.concat(th[seeds2[q][0][i],seeds2[q][1][i]],th_init))
    th = th.astype(int)
       
    zs_big = z
    ths_big= th
    i += 1
    max_run_values = frac_pond - 1
    
    return zs_big, ths_big, i, max_run_values
